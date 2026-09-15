# Tech Landscape

*Last Updated: 2026-09-15*

No repo-wide language or package manager. Each plugin is its own stack — see
[plugins.md](plugins.md) for identity/purpose context.

## Repo root scaffolding

- Python (`scripts/new_hook.py`, `scripts/test_hooks.py`) — `uv run --script` PEP 723 standalone
  scripts, zero shared deps.
- JSON test fixtures (`tests/payloads/*.json`), one per hook lifecycle event.
- Markdown memory scratch files (`.todo/*.md`) — Serena/memory-agent-style notes (`mem:tech_stack`,
  `mem:conventions`, etc.), not project config; safe to ignore for build/run purposes.

## `plugins/skoghooks/`

- **Python ≥3.11 (mostly)**, some scripts (`pre_tool_use.py`, `post_tool_use.py`) only require ≥3.8.
  No shared `pyproject.toml`/lockfile — every `scripts/*.py` hook is a standalone `uv run --script`
  entry point with inline PEP 723 `# dependencies = [...]` metadata.
  Source of truth for versions: read each script's own header, not a single repo-wide constraint.
- **Node.js (undocumented)** — `scripts/hooks/*.js` and `scripts/lib/*.js` (137 files, 72% of the
  plugin), CommonJS (`require`, `'use strict'`), no `package.json` found. See
  [plugins.md](plugins.md#skoghooks-drift-from-claudemd).
- Optional local **Ollama** integration (`user_prompt_submit.py --name-agent`), model via
  `OLLAMA_MODEL` env (default `gpt-oss:20b`), degrades silently if unavailable.
- Testing: `scripts/test_hooks.py` (root) pipes `tests/payloads/*.json` through every wired command,
  asserts exit 0; plugin also has its own `tests/*.bats` (Bats shell tests).

## `plugins/skogharness/`

- **Node.js, dependency-free** — every `scripts/hooks/*.js` and `scripts/lib/*.js` file uses only
  Node built-ins (`fs`, `path`), CommonJS, `#!/usr/bin/env node`. No `package.json` anywhere in the
  plugin — deliberate, so it works regardless of the host project's package manager (there's even
  `scripts/setup-package-manager.js` to *detect*, not install, a package manager).
  Zero test coverage for this half of the codebase (~most of the 666 files) — no test runner config,
  no `*.test.js` found.
- **Python** — two files: `skills/skogai/continuous-learning-v2/scripts/instinct-cli.py` (1956 lines,
  the single largest file in the entire repo) with its own test `test_parse_instinct.py` (1421 lines,
  likely run via plain `pytest`, no pytest config file confirmed), plus
  `scripts/lib/ecc_dashboard_runtime.py`.
- Content authoring: Markdown + YAML frontmatter (67 agent defs, 92 command defs, ~80+37 skill defs
  across two formats), JSON (hooks.json, manifests, per-language rule configs).

## `plugins/skogix-hooks/` (`dot-core`)

- **Bash** — all 6 wired hooks (`hooks/*.sh`) plus `scripts/*.sh` shared helpers.
- **Python 3 stdlib** — `hooks/lesson_matcher.py` (377 lines, YAML-frontmatter lesson matching, with a
  fallback hand-rolled YAML parser if `pyyaml` is unavailable). Tested via
  `uvx pytest hooks/test_lesson_matcher.py`.
- **jq** — the `skills/skogai-jq/` transform library (1083 files, ~70 transform directories), each
  transform a standalone `.jq` file with a `schema.json` and `test.sh`, explicitly dependency-free by
  design "for AI agent discoverability."
- **Bats** — shell test suites under `tests/*.bats`.
- No `package.json`/`pyproject.toml`/`go.mod` anywhere — its own `AGENTS.md` explicitly forbids adding
  a build-step manifest at the plugin level.

## `plugins/skogix-core-original/` (`skogai-routing`)

- Pure **Markdown + JSON Schema**. A handful of Bash/Python validator scripts
  (`scripts/_validate_file.py`, `scripts/validate-schema.sh`, `scripts/list-xml-tags.sh`,
  `scripts/create-gh-issue.sh`). No runtime dependencies, no hooks, no lifecycle wiring.

## Cross-cutting observation

Every hook-bearing plugin independently reinvents "no shared dependency manifest, standalone scripts
only" — this looks like a deliberate house convention across the SkogAI ecosystem (each plugin must
be installable/copyable without a build step), not an accident repeated four times. Confirm before
adding a `package.json`/`pyproject.toml` to any of these trees; it likely violates the pattern.
