---
permalink: skogai/claude
type: router
---

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

<routes>

- @SKOGAI.md

</routes>

## What this repo is

`skogai-harness` is a **meta-repo**: it builds and tests *harnesses* — the
runtime layer wrapped around a model (Claude Code first, `codex cli` as the
"beta tester"). It is not an application. It contains two intertwined things:

1. A **blueprint / pattern framework** for harness design — the concept doc and
   pattern language under `.docs/` (`what-is-a-harness.md` is the front door).
2. A **Claude Code plugin marketplace + skills + hooks + validators** that are
   the concrete, testable artifacts of that framework.

The organizing idea (see `.docs/what-is-a-harness.md`): a harness is defined by
its *planes* — request assembly, turn loop, tool plane, memory plane, recovery,
human control, extension plane. Changes here should map to one of those planes.

`.specify/memory/constitution.md` is the ratified policy behind all of this
(five principles: bare-baseline A/B attribution, plane-based design, meta-repo
scope discipline, router-pattern integrity, fail-closed validation). Read it
before arguing that a rule here is arbitrary — most of them are derived from it.

### The bare baseline (central concept)

To prove a harness addition (system prompt, tools, settings, mcp, skills, hooks)
actually changes behavior, the repo pins a zero-config Claude instance as a diff
baseline. A/B behavior is tested with `claude --safe-mode --system-prompt ""
--tools "" --setting-sources "" --strict-mcp-config --disable-slash-commands
--settings .claude/settings.bare.json`, then dialing single "knobs" back on
(`--append-system-prompt`, `--allowedTools`, `--mcp-config`,
`--permission-mode`, …). The settings file is meant to be `{}` — the emptiness
is the proof, not a config to fill in. Full knob table in
`.docs/what-is-a-harness.md`.

> **Known drift (verify before relying on it):** `.claude/settings.bare.json`
> does **not** exist in the tracked tree, although `.docs/what-is-a-harness.md`
> links to it, the constitution names it, and this file describes it. That gap
> is the motivating example of the active spec
> `specs/001-truthfulness-rebaseline` (FR-002 requires the file to exist and
> contain `{}`). Don't quietly delete the references, and don't assume the
> baseline is runnable as written.

## Toolchain & commands

Environment is declared in `mise.toml` (node 26, bun 1.3.14, python 3.14, uv).

```sh
mise trust && mise install     # fresh clone setup
```

**Do not trust `mise run check` as a gate.** It depends on `test` + `test:py`,
and both legs are hollow — this is exactly the false-green that
`specs/001-truthfulness-rebaseline` (User Story 2) exists to fix:

- `mise run test` (`node --test`) resolves to **0 tests** from the root: node's
  default globber skips the hidden `.claude/` dir where the `.test.js` files
  live. It still exits 0.
- `mise run test:py` runs in `scripts/`, which contains only
  `match-lessons.py` and **no test files at all**. The real Python suite lives
  in `.scripts/`.

**Run these directly instead — these are the suites that actually assert things:**

```sh
# Python validators (.scripts/) — the real Python test suite, 25 tests.
python3 -m unittest discover -s .scripts -p 'test_*.py'

# skoghooks plugin hook smoke test — pipes every fixture through every wired
# hook; every hook must exit 0. Currently 14/14.
uv run marketplace/scripts/test_hooks.py
uv run marketplace/scripts/test_hooks.py --event Stop   # single event

# TS hooks (.claude/hooks/) have their own package.json:
cd .claude/hooks && npm install && npm run check   # tsc --noEmit

# Node test files under .claude/ need a quoted glob (a bare directory arg
# makes node try to load it as a module). Run `npm install` in that dir first
# — the suite has its own package.json and needs `ws`.
node --test '.claude/tests/brainstorm-server/*.test.js'
```

That suite is 7 tests, of which **5 pass and 2 fail on a clean checkout**
(`branding.test.js` expects a `.claude/package.json` that doesn't exist;
`server.test.js` also fails). Treat those two as pre-existing, not as something
you broke.

`.claude/tests/` holds nine suites, not just `brainstorm-server/` — also
`claude-code/`, `codex/`, `codex-plugin-sync/`, `explicit-skill-requests/`,
`hooks/`, `opencode/`, `pi/`, `shell-lint/`. Most are shell harnesses;
`.claude/tests/claude-code/run-skill-tests.sh` shells out to a real `claude`
binary and is slow (10-min default timeout per test).

### Running the validators directly (read this before "fixing" a failure)

The `.scripts/` validators are **fail-closed against a distribution layout**,
not against this repo's tree. Run bare from the repo root, several *fail by
design* because the layout they audit isn't here — that is not a regression to
chase:

| Command | Bare result from repo root |
|---|---|
| `python3 .scripts/check_skill_language.py` | passes |
| `python3 .scripts/check_reference_neutrality.py` | passes |
| `python3 .scripts/check_skill_closure.py` | passes |
| `python3 .scripts/validate_skill_quality.py` | fails: wants a top-level `skills/` dir |
| `python3 .scripts/check_profile_consistency.py` | fails: wants `references/harness-profiles.json` |
| `python3 .scripts/validate_plugin_metadata.py` | fails: wants `.codex-plugin/plugin.json` (takes an optional `root` arg) |
| `python3 .scripts/validate_router.py` | exits 2: needs `uv run` for its deps, and then still crashes (see below) |

`validate_router.py` is **currently unrunnable from this repo**, and it takes
explicit file args. Under `uv run` it gets past the `jsonschema`/`pyyaml`
import guard and then raises `FileNotFoundError` on
`templates/schemas/router.schema.json` — it resolves `SCRIPT_DIR/../templates/
schemas/`, but the schemas actually live in `.skogix/schemas/`. It is also the
one validator with no colocated test, which is precisely why this went
unnoticed; that pairing rule below exists to prevent exactly this.

The colocated `test_*.py` files — which build their own temp fixture roots —
are the real check on validator behavior.

`./.scripts/check-skills.sh` has a path bug: it derives the project dir as
`$SCRIPT_DIR/../..`, which overshoots from `.scripts/` to the repo's *parent*
and reports `ERROR: Skills directory not found: ~/.claude/skills`. Work around
it (or fix it) with:

```sh
CLAUDE_PROJECT_DIR="$PWD" ./.scripts/check-skills.sh
```

**Plugin validation:**

```sh
claude plugin validate ./marketplace/plugins/skoghooks
claude plugin validate ./marketplace                    # the marketplace itself
claude --plugin-dir ./marketplace/plugins/skoghooks     # test locally, no install
```

## Repository map

| Path | Purpose |
|---|---|
| `.docs/` | Harness concept + pattern language (`what-is-a-harness.md`, `harness/`, `archive/`). The design source of truth. |
| `.specify/`, `specs/` | Spec-kit workflow: ratified `memory/constitution.md`, templates, scripts; `specs/` holds active feature specs. Driven by the `speckit-*` skills (`specify` → `plan` → `tasks` → `implement`). |
| `marketplace/` | Claude Code plugin marketplace. Has its own `CLAUDE.md` + `AGENTS.md` — read them before touching plugins. |
| `marketplace/plugins/` | `skoghooks` (13-event hook reference impl), `skogharness`, `skogix-core-original`, `skogix-hooks`. |
| `.claude/` | The **active** local harness config: `settings.json` (wires hooks + a permission allowlist), `skills/`, `hooks/` (TS), `agents/`, `commands/`, `scripts/`, `tests/`. |
| `.scripts/` | Validation & maintenance domain (skill quality, reference neutrality, router/plugin-metadata/profile validators). See `.scripts/AGENTS.md` — note its examples say `scripts/`, but the files are in `.scripts/`. |
| `scripts/` | `match-lessons.py` only. Not a test directory, despite `mise run test:py`. |
| `.skogix/` | JSON `schemas/` (agent, skill, router, lesson, workflow, …) and `todo/gsd-planning/` planning workspace. |
| `.agents/`, `.codex/` | Cross-tool mirrors (codex cli is the "beta tester" for harness features). |
| `todo/drafts/` | Pre-spec planning drafts; specs are formalized from these. |
| `CLAUDE.md`, `SKOGAI.md`, `AGENTS.md` | Live agent-instruction router files — must stay at their paths (`.docs/README.md`, "Not moved here"). |

## Two distinct hook systems (don't conflate them)

- **skoghooks plugin** (`marketplace/plugins/skoghooks/scripts/*.py`): the 13
  lifecycle hooks, Python + inline PEP 723 metadata (`#!/usr/bin/env -S uv run
  --script`), wired into `.claude/settings.json` via `$CLAUDE_PROJECT_DIR/...`.
  Add hooks with the `/new-hook` skill or `marketplace/scripts/new_hook.py`.
  Every hook must exit 0; exit 2 only to deliberately block. Runtime logs go to
  `<tmp>/skoghooks/<session_id>/`, never into the repo. Full detail:
  `marketplace/CLAUDE.md`.
- **TS hook toolkit** (`.claude/hooks/`): TypeScript hooks for skill
  auto-activation, session-doc updating, and `tsc` checks — its own
  `package.json` (better-sqlite3, minimatch; optional LLM SDKs for
  classification), run via `tsx`. Independent of the plugin above.

## Conventions

- **Router pattern.** `CLAUDE.md` → `@SKOGAI.md`; docs use `<routes>` blocks with
  `@path` links, above YAML frontmatter (`permalink`, `type: router`). Preserve
  that shape when editing router files rather than inlining content. Note
  `SKOGAI.md`'s `<routes>` block is currently an empty bullet — a dead end, and
  in scope for the truthfulness spec.
- **The three router files are mirrors, and the mirroring is lossy.**
  `AGENTS.md` is a search-and-replaced copy of `CLAUDE.md` for codex; the
  substitution has been applied blindly, so it contains artifacts like
  `.Codex/settings.bare.json` and "Codex (Codex.ai/code)". When you change
  `CLAUDE.md`, decide deliberately what `AGENTS.md` should say — don't re-run a
  naive replace.
- **Validators are policy.** `check_reference_neutrality.py` and
  `check_skill_language.py` encode distribution policy for the public surface —
  don't broaden their allowlists just to make a check pass.
- **New Python validator ⇒ colocated `test_<name>.py`** in `.scripts/`, using
  `unittest` + temp dirs + dynamic sibling-module loading (not package imports).
  `validate_router.py` is the one pre-existing exception.
- **Prefer fixing a documented command over documenting the workaround.** This
  repo's stated purpose is that its own claims be checkable; a false-green
  command or a doc pointing at a missing file is a bug in the product, not a
  quirk to route around.
- **Runtime artifacts are gitignored:** `.claude/data/sessions`,
  `.claude/worktrees`, `/tmp`, `.skogai/config/backups`,
  `.skogai/config/script_metadata.json`. Don't treat them as committed state.
  `.gitignore` does **not** cover `node_modules/` or `__pycache__/`, both of
  which the commands above generate — don't let them into a commit.
