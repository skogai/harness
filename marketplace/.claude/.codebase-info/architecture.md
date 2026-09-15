# Architecture

*Last Updated: 2026-09-15*

## System overview

This repo is a **Claude Code marketplace** at its root (`.claude-plugin/marketplace.json`), but has
grown into a monorepo bundling four independently-developed, plugin-shaped projects under `plugins/`.
There is no shared build system, no shared dependency manifest, and no shared runtime across them —
each is its own island. See [plugins.md](plugins.md) for the full catalog; this doc covers how they
relate structurally.

```
harness/marketplace/                    (this repo — a Claude Code marketplace)
├── .claude-plugin/marketplace.json     ← registers ONLY plugins/skoghooks
├── CLAUDE.md, AGENTS.md, README.md     ← document plugins/skoghooks in detail; silent on the other 3
├── scripts/  templates/  tests/        ← scaffolding for skoghooks (new_hook.py, hook_template.py, fixtures)
├── .todo/                              ← memory-agent scratch notes (Serena-style mem:* files), not code
└── plugins/
    ├── skoghooks/          ← REGISTERED. 13-event Python hook reference impl + undocumented ECC-JS subsystem
    ├── skogharness/        ← UNREGISTERED. Vendored "Everything Claude Code" — own marketplace.json
    ├── skogix-hooks/       ← UNREGISTERED. "dot-core" — Codex-schema hook/skill incubator, no .claude-plugin
    └── skogix-core-original/  ← UNREGISTERED. Not a plugin — a Skill (routing meta-framework)
```

## Why this matters for changes

- **A change inside `plugins/skoghooks/`** is the only one that affects what `/plugin install
  skoghooks@skoghooks` actually installs from this repo. Validate with
  `claude plugin validate ./plugins/skoghooks` and `claude plugin validate .` (root).
- **A change inside `plugins/skogharness/`** affects a self-contained vendored project with its own
  marketplace.json — it would be installed via `/plugin marketplace add ./plugins/skogharness`
  directly, bypassing the root catalog entirely. Its internal "ECC" naming suggests upstream sync is
  still in progress; don't assume repo-root conventions (e.g. root `AGENTS.md`'s hook-wiring gotchas)
  apply to it.
- **A change inside `plugins/skogix-hooks/`** affects an explicitly-labeled incubator (`dot-core`) for
  a *different* hook schema (Codex's 6-event model, not Claude Code's 13-event model). Its `AGENTS.md`
  states hooks/skills here get promoted to standalone plugins later — don't assume it's installable
  as-is via Claude Code's plugin system (it has no `.claude-plugin/plugin.json`).
- **A change inside `plugins/skogix-core-original/`** affects a documentation/routing skill, not
  runtime hook behavior — it has no lifecycle wiring at all.

## Two independent "ECC" Node.js subsystems

Both `plugins/skoghooks/scripts/{hooks,lib}/*.js` (137 files) and `plugins/skogharness/scripts/`
(Node hook dispatchers + libs, ~138 files) contain what looks like the same "Everything Claude Code"
observability/orchestration tooling (env vars like `ECC_GOVERNANCE...`, files named
`ecc-metrics-bridge.js`, `ecc-context-monitor.js`, a `memory-persistence` sub-hook-system, a
`control-pane` mini dashboard). Whether these are two copies of the same vendored codebase or diverged
forks was not verified file-by-file — treat as a strong hypothesis, not a confirmed fact, and diff the
two trees before assuming either is canonical if you need to change ECC-related code.

## Data flow: hook lifecycle (the pattern all 3 hook-bearing plugins share)

Claude Code (or Codex, for `skogix-hooks`) emits a JSON payload on stdin to a wired command at a
lifecycle event (SessionStart, PreToolUse, PostToolUse, Stop, etc.). Each plugin's hook script:

1. Reads/parses the stdin JSON payload.
2. Does its narrow job (log an event, inject `additionalContext`, or — rarely — block via exit 2).
3. Exits 0 in the overwhelming majority of cases; a non-zero exit is reserved for deliberate blocking
   and is used sparingly (see [patterns.md](patterns.md) for the fail-open convention shared across
   `skoghooks` and `skogix-hooks`).

Runtime state (logs, transcript backups, session data) is written to a **tmp directory scoped by
session id**, never committed to the repo — `plugins/skoghooks/scripts/utils/runtime_dir.py` resolves
`$CLAUDE_CODE_TMPDIR/skoghooks/<session_id>/` (fallback `/tmp/skoghooks/<session_id>/`);
`skogix-hooks` writes ad hoc to `/tmp/${session_id}.jsonl` in a couple of scripts.

## What's NOT shared across plugins

- No shared `package.json`/`pyproject.toml`/lockfile anywhere in the repo — each plugin manages its
  own dependencies inline (Python: PEP 723 `uv run --script` headers; Node: dependency-free stdlib
  only; jq: no deps by design).
- No shared test runner — `skoghooks` uses `scripts/test_hooks.py` (root) + its own `.bats`;
  `skogix-hooks` uses Bats + pytest; `skogharness` has effectively one Python test file and no JS
  tests; `skogix-core-original` has shell/Python validator scripts, not a test suite.
- No shared linter/formatter config at repo root.
