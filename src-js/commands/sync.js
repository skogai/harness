import chalk from 'chalk';
import { readFile, writeFile } from 'fs/promises';
import { pathExists } from 'fs-extra';
import { join, resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import {
  copyAgentEssentials,
  copyAgentSkills,
  copyCommands,
  copyToonUtils,
  getSkillSummaries,
} from '../utils/copy.js';
import { setupToonBinary } from '../utils/toon.js';
import { upsertManagedBlock } from '../utils/managed-block.js';
import { loadManifest, resolveManifest, MANIFEST_FILENAME } from '../manifest.js';
import { buildMcpServersMap, buildCodexMcpToml, collectEnvReferences } from '../mcps.js';
import { formatAgentTargets } from '../agents.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BLOCKS_DIR = join(__dirname, '../../templates/blocks');

async function readJsonIfExists(filePath) {
  if (!(await pathExists(filePath))) {
    return null;
  }
  try {
    return JSON.parse(await readFile(filePath, 'utf-8'));
  } catch (error) {
    throw new Error(`Failed to parse ${filePath}: ${error.message}`, { cause: error });
  }
}

/**
 * Merge managed MCP entries into an existing mcpServers JSON file by key.
 * Keys harness did not write are preserved untouched; managed keys
 * are overwritten to match skogai.json.
 */
async function writeMcpServersJson(filePath, mcps) {
  if (mcps.length === 0) {
    return null;
  }
  const existing = (await readJsonIfExists(filePath)) || {};
  existing.mcpServers = { ...(existing.mcpServers || {}), ...buildMcpServersMap(mcps) };
  await writeFile(filePath, `${JSON.stringify(existing, null, 2)}\n`, 'utf-8');
  return filePath;
}

async function renderBlockTemplate(name, replacements) {
  let content = await readFile(join(BLOCKS_DIR, name), 'utf-8');
  for (const [key, value] of Object.entries(replacements)) {
    content = content.replaceAll(`{{${key}}}`, value);
  }
  return content;
}

async function buildClaudeSkillsBlock(skills) {
  const summaries = await getSkillSummaries(skills);
  const skillList = summaries.map((skill) => `- \`${skill.id}\`: ${skill.description}`).join('\n');
  return renderBlockTemplate('claude-skills.md', { SKILLS: skillList || '- No skills installed.' });
}

async function buildCodexBlock(skills) {
  const summaries = await getSkillSummaries(skills);
  const skillList = summaries.map((skill) => (
    `- \`${skill.id}\`: ${skill.description}\n  Read \`.codex/skills/${skill.id}/SKILL.md\` before using this skill.`
  )).join('\n');
  return renderBlockTemplate('codex-skills.md', { SKILLS: skillList || '- No skills installed.' });
}

async function syncClaude(targetDir, plan, options) {
  // force stays false: an existing settings.json is user-owned after install
  await copyAgentEssentials(targetDir, 'claude', { ...options, force: false });
  await copyAgentSkills(targetDir, 'claude', plan.skills, { ...options, force: true });

  if (plan.commands.length > 0) {
    await copyCommands(targetDir, plan.commands, { ...options, force: true });
  }
  if (plan.toon) {
    await copyToonUtils(targetDir, { ...options, force: true });
    const toonResult = setupToonBinary(resolve(targetDir, '.claude'));
    if (!toonResult.success) {
      throw new Error(toonResult.error);
    }
  }

  await upsertManagedBlock(
    join(targetDir, 'CLAUDE.md'),
    'harness:skills',
    await buildClaudeSkillsBlock(plan.skills),
  );
  return writeMcpServersJson(join(targetDir, '.mcp.json'), plan.mcps);
}

async function syncCodex(targetDir, plan, options) {
  await copyAgentEssentials(targetDir, 'codex', { ...options, force: true });
  await copyAgentSkills(targetDir, 'codex', plan.skills, { ...options, force: true });
  await upsertManagedBlock(
    join(targetDir, 'AGENTS.md'),
    'harness:skills',
    await buildCodexBlock(plan.skills),
  );
  if (plan.mcps.length > 0) {
    await upsertManagedBlock(
      join(targetDir, '.codex', 'config.toml'),
      'harness:mcp',
      buildCodexMcpToml(plan.mcps),
      { commentPrefix: '#' },
    );
  }
}

const TARGET_SYNCERS = {
  claude: syncClaude,
  codex: syncCodex,
};

async function updateEnvExample(targetDir, envVars) {
  if (envVars.length === 0) {
    return { added: [] };
  }
  const envExamplePath = join(targetDir, '.env.example');
  const existing = (await pathExists(envExamplePath))
    ? await readFile(envExamplePath, 'utf-8')
    : '';
  const missing = envVars.filter((name) => !new RegExp(`^${name}=`, 'm').test(existing));
  if (missing.length === 0) {
    return { added: [] };
  }
  const block = [
    '',
    '# MCP servers (skogai.json — used by harness sync targets)',
    ...missing.map((name) => `${name}=`),
    '',
  ].join('\n');
  await writeFile(envExamplePath, existing + block, 'utf-8');
  return { added: missing };
}

export async function runSync(dir = '.', options = {}) {
  const targetDir = resolve(dir);
  const manifest = await loadManifest(targetDir);
  if (!manifest) {
    throw new Error(`No ${MANIFEST_FILENAME} found in ${targetDir}. Run \`npx --yes github:skogai/harness init\` first.`);
  }
  const plan = resolveManifest(manifest);

  for (const target of plan.targets) {
    await TARGET_SYNCERS[target](targetDir, plan, options);
  }

  const envVars = collectEnvReferences(plan.mcps);
  const { added } = await updateEnvExample(targetDir, envVars);
  const unsetVars = envVars.filter((name) => !process.env[name]);

  return { plan, envVars, addedEnvExampleVars: added, unsetVars };
}

export async function sync(dir = '.', options = {}) {
  try {
    const { plan, addedEnvExampleVars, unsetVars } = await runSync(dir, options);
    console.log(chalk.green(
      `Synced ${plan.skills.length} skills and ${plan.mcps.length} MCP servers for ${formatAgentTargets(plan.targets)}`,
    ));
    if (plan.profile) {
      console.log(chalk.dim(`Profile: ${plan.profile}`));
    }
    if (addedEnvExampleVars.length > 0) {
      console.log(chalk.dim(`Added to .env.example: ${addedEnvExampleVars.join(', ')}`));
    }
    if (unsetVars.length > 0) {
      console.log(chalk.yellow(`Unset env vars referenced by MCPs: ${unsetVars.join(', ')}`));
    }
  } catch (error) {
    console.error(chalk.red(`Sync failed: ${error.message}`));
    process.exit(1);
  }
}
