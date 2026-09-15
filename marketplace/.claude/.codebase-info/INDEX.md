# Codebase Map — skoghooks marketplace

*Last Updated: 2026-09-15*

## What this repo actually is

The root `CLAUDE.md`/`README.md` describe this as "a reference implementation of all 13
Claude Code hook lifecycle events." That is true of **one plugin** here —
[`plugins/skoghooks/`](#) — but the repo has grown into a **monorepo bundling four
unrelated Claude-Code-plugin-shaped projects**, only one of which is actually registered
in the root marketplace catalog. See [architecture.md](architecture.md) for the full
picture and [plugins.md](plugins.md) for a per-plugin catalog — read that second doc
before assuming anything about "the plugin" singular.

Quick orientation:

| Doc | Read it for |
|---|---|
| [architecture.md](architecture.md) | The monorepo-of-plugins structure, what's registered vs. vendored-but-orphaned |
| [plugins.md](plugins.md) | Catalog of all 4 plugin dirs: identity, registration status, size, purpose |
| [tech-landscape.md](tech-landscape.md) | Languages/runtimes per plugin (Python uv-scripts, dependency-free Node, Bash+jq) |
| [directory-structure.md](directory-structure.md) | Annotated tree, repo root + each plugin |
| [entry-points.md](entry-points.md) | hooks.json wiring for each of the 4 plugins |
| [modules.md](modules.md) | Key scripts/modules per plugin, the biggest/most central files |
| [patterns.md](patterns.md) | Cross-cutting conventions: fail-open hooks, exit-code contract, AGENTS.md routers |
| [onboarding.md](onboarding.md) | How to test/validate/install each plugin locally |

## Key facts to hold in your head

1. **Only `plugins/skoghooks/` is in the root marketplace catalog** (`.claude-plugin/marketplace.json`
   lists exactly one plugin entry: `skoghooks`). `plugins/skogharness/`, `plugins/skogix-hooks/`,
   and `plugins/skogix-core-original/` all live in `plugins/` but are **not** installable via this
   repo's marketplace — confirmed intentional (root `AGENTS.md` says so explicitly), not an oversight.
2. **`plugins/skoghooks/` itself has undocumented content**: 72% of its 189 tracked files (137 files
   under `scripts/hooks/*.js` and `scripts/lib/*.js`) are a Node.js "ECC" subsystem the root
   `CLAUDE.md` never mentions. Don't trust `CLAUDE.md`'s file tree as exhaustive — see
   [plugins.md](plugins.md#skoghooks-drift-from-claudemd).
3. **`plugins/skogharness/` is a vendored copy of "Everything Claude Code" (ECC)**, a much larger
   third-party-style plugin (67 agents, 92 commands, ~120 skill folders across two formats). Internal
   code still says "ECC" (env vars, filenames). It has its own `.claude-plugin/marketplace.json`,
   independent of the repo root's.
4. **`plugins/skogix-hooks/` is really named `dot-core`** (per its `.codex-plugin/plugin.json` — it
   has no `.claude-plugin/plugin.json` at all) and targets a different, Codex-style hook schema
   (6 events, not 13). 1093 of its 1154 files are the `skogai-jq` jq-transform library.
5. **`plugins/skogix-core-original/` isn't a hook plugin at all** — no `plugin.json`/`.claude-plugin/`
   anywhere. It's a Claude Code *Skill* (`SKILL.md`, `type: router`) implementing a documentation/
   routing meta-framework, orthogonal to the other three.

## How to use this map

Read [plugins.md](plugins.md) first if you're not sure which of the 4 plugin directories a task
concerns — the four are unrelated in purpose, language, and lifecycle-event schema. Then jump to the
plugin-specific sections in [entry-points.md](entry-points.md) / [modules.md](modules.md).

## How to maintain this map

Run the `update-codebase-map` skill after material changes (new plugin added, marketplace.json
registration changed, a plugin's hook wiring changed). This map was seeded via the large-codebase
inline-parallel-exploration path (4 sub-agents, one per `plugins/*` directory) because Sidequest
tooling was unavailable in the mapping session — file counts and structural claims were sampled, not
exhaustively verified against every file, especially inside `skills/skogai-jq/` (1083 files) and
`plugins/skogharness/` (666 files).
