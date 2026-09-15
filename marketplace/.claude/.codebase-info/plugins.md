# Plugin Catalog

*Last Updated: 2026-09-15*

The repo root is a Claude Code **marketplace** (`.claude-plugin/marketplace.json`). `plugins/`
contains four directories that each look like a Claude Code plugin, but they differ sharply in
identity, registration status, purpose, and tech stack. Treat each as a separate codebase.

## Registration status (root `.claude-plugin/marketplace.json`)

```json
{
  "name": "skoghooks",
  "plugins": [ { "name": "skoghooks", "source": "./plugins/skoghooks", ... } ]
}
```

Only **one** entry. The other three plugin directories exist on disk but are not reachable via
`/plugin marketplace add ./` + `/plugin install <name>@skoghooks` from repo root. Root `AGENTS.md`
confirms this is deliberate: "The distributable plugin lives in `plugins/skoghooks/`; the root
`.claude-plugin/marketplace.json` only points marketplace installs at that plugin."

| Directory | Files (git-tracked) | Has `.claude-plugin/plugin.json`? | In root marketplace.json? | Real identity |
|---|---|---|---|---|
| `plugins/skoghooks/` | 189 | Yes | **Yes — the only one** | "skoghooks" — 13-hook Python reference impl (+ undocumented JS) |
| `plugins/skogharness/` | 666 | Yes (own, separate marketplace.json too) | No | "Everything Claude Code" (ECC), vendored/rebranded |
| `plugins/skogix-hooks/` | 1154 | **No** — only `.codex-plugin/plugin.json` | No | `dot-core` — SkogAI hook/skill incubator, Codex-schema |
| `plugins/skogix-core-original/` | 35 | **No** — no plugin manifest at all | No | `skogai-routing` — a Claude Code *Skill*, not a plugin |

## `plugins/skoghooks/` — the registered plugin

Reference implementation of all 13 Claude Code hook lifecycle events, in Python via `uv run --script`
(PEP 723 inline deps, no shared `pyproject.toml`). Fully documented in root `CLAUDE.md` — see that
file for the hook-event → script table and flag reference; don't duplicate it here.

### skoghooks: drift from CLAUDE.md

Verified against the live tree; CLAUDE.md is **not exhaustive**:

- **72% of the plugin's files (137 of 189) are an undocumented Node.js subsystem**:
  `scripts/hooks/*.js` (49 files — `session-start-bootstrap.js`, `observe-runner.js`,
  `cost-tracker.js`, `ecc-*.js`, `github-coordination*.js`, `control-pane/*`) and `scripts/lib/*.js`
  (~88 files — `install-targets/`, `session-adapters/`, `state-store/`, `skill-evolution/`,
  `worktree-lifecycle/`). This looks like the same "ECC" observability/orchestration tooling found in
  `plugins/skogharness/`, living here too. CLAUDE.md's tree diagram never mentions it.
- `hooks/hooks.json`'s top-level `"hooks"` key nests a second `"description"`/`"events"` block
  referencing those `.js` files ("Reference lifecycle hook definitions for ECC memory persistence"),
  spliced in alongside the real 13 per-event Python wiring. It duplicates a separate
  `memory-persistence/hooks.json` (which has its own README). Appears to be dead/reference-only, not
  live wiring, but sits in the production file.
- `.claude/skills/new-hook/` and `.claude/settings*.json`, both documented in CLAUDE.md's tree, **do
  not exist anywhere in the repo** (`git ls-files .claude` is empty at repo root).
- `hooks/` also contains undocumented `lesson_matcher.py`, `test_lesson_matcher.py`, and
  `user-prompt-submit.sh`. The `UserPromptSubmit` event actually fires **two** commands:
  `user_prompt_submit.py --log-only` (per CLAUDE.md — though `--name-agent` from the doc's flag table
  is not actually wired) **plus** `hooks/user-prompt-submit.sh` (undocumented).
- Python version requirement isn't uniformly `>=3.11` as CLAUDE.md's example header implies:
  `session_start.py`/`notification.py` require `>=3.11`; `pre_tool_use.py`/`post_tool_use.py` require
  only `>=3.8`.
- The plugin has its own `plugins/skoghooks/tests/*.bats` (`skogai-jq.bats`, `user-prompt-submit.bats`)
  — a second test suite alongside the root `scripts/test_hooks.py`, not mentioned by CLAUDE.md.
- `utils/` and `validators/` — everything CLAUDE.md claims here checks out exactly (see
  [modules.md](modules.md)).

## `plugins/skogharness/` — vendored "Everything Claude Code"

`.claude-plugin/plugin.json` says `"skogharness"`, but the plugin's own `AGENTS.md` opens with
"Everything Claude Code (ECC) — Agent Instructions... a production-ready AI coding plugin providing
67 specialized agents, 277 skills, 92 commands, and automated hook workflows." Internal code/env vars
still say `ECC_*` and filenames like `ecc-metrics-bridge.js` — this is a rebrand-in-progress of a
third-party-style plugin, not something authored fresh for this repo.

Has its own `.claude-plugin/marketplace.json` (category `"workflow"`, owner skogix), independent of
the repo-root one — meaning it's designed to be added as a *separate* marketplace if someone points
`/plugin marketplace add` at `plugins/skogharness/` directly, not through the repo root.

Full detail in [modules.md](modules.md#skogharness) and [entry-points.md](entry-points.md#skogharness).

Notable: a **dual skill format** lives side by side — `skills/skogai/*` (native Claude Code SKILL.md,
~80 folders) and `.agents/skills/*` (OpenAI-agent-format `agents/openai.yaml` mirror, 37 folders) plus
`.agents/plugins/marketplace.json` — evidence of a deliberate multi-runtime portability goal (an
install subsystem in `scripts/lib/install-targets/*.js` pushes config into 9+ AI coding tools: Claude,
Cursor, Codex, Gemini, Zed, OpenCode, Qwen, JoyCode, CodeBuddy, Antigravity).

## `plugins/skogix-hooks/` — `dot-core`

Not a `.claude-plugin` at all — its manifest is `.codex-plugin/plugin.json` (name `dot-core`, v0.0.4):
"SkogAI base plugin for building and testing reusable hooks, skills, agent prompts, and tool
integrations" — an **incubator**, not a finished distributable. Its own `AGENTS.md` calls it "a local
place to be developed, loaded, tested, and promoted before they become standalone plugins."

Targets a **6-event Codex hook schema** (SessionStart, UserPromptSubmit, PreToolUse,
PermissionRequest, PostToolUse, Stop) via `hooks.json` → `hooks/*.sh`, not the 13-event Claude Code
schema `plugins/skoghooks/` uses. 11 more hook scripts exist unwired in `hooks/` (pre-compact.sh,
session-end.sh, subagent-*.sh, etc.) because the Codex schema doesn't support those events yet.

1093 of its 1154 files are `skills/skogai-jq/` — a jq-transform library (~70 transform directories:
`crud-get`, `array-filter`, `extract-urls`, `validate-*`, `to-*`, `is-*`, each with `transform.jq`,
`schema.json`, `test.sh`, and 8-25 JSON fixtures), explicitly designed "for AI agent discoverability"
per its own docs.

Full detail in [modules.md](modules.md#skogix-hooks-dot-core) and
[entry-points.md](entry-points.md#skogix-hooks-dot-core).

## `plugins/skogix-core-original/` — `skogai-routing`

No plugin manifest anywhere in the directory (confirmed via `find`). Entry point is `SKILL.md`
(frontmatter `name: skogai-routing`, `type: router`): "Routes information through a progressive
framework of routing files, workflows, references, templates, and scripts." It's a meta-framework
teaching *how to structure* routing/reference/template/workflow/schema files for any agent-facing
repo — self-referential tooling, not a runtime capability like the other three.

Structure: `references/` (5 durable-concept docs), `workflows/` (9 ordered procedures),
`templates/` (6 output shapes), `schemas/` (12 JSON Schemas + README), `scripts/` (4 shell/Python
validators). Pure Markdown + JSON Schema, no hooks, no lifecycle wiring.
