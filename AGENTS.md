---
permalink: skogai/Codex
type: router
---

# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

<routes>

- @SKOGAI.md

</routes>

## What this repo is

`skogai-harness` is a **meta-repo**: it builds and tests *harnesses* — the
runtime layer wrapped around a model (Codex first, `codex cli` as the
"beta tester"). It is not an application. It contains two intertwined things:

1. A **blueprint / pattern framework** for harness design — the concept doc and
   pattern language under `.docs/` (`what-is-a-harness.md` is the front door).
2. A **Codex plugin marketplace + skills + hooks + validators** that are
   the concrete, testable artifacts of that framework.

The organizing idea (see `.docs/what-is-a-harness.md`): a harness is defined by
its *planes* — request assembly, turn loop, tool plane, memory plane, recovery,
human control, extension plane. Changes here should map to one of those planes.

### The bare baseline (central concept)

To prove a harness addition (system prompt, tools, settings, mcp, skills, hooks)
actually changes behavior, the repo keeps a zero-config Codex instance as a
diff baseline. `.Codex/settings.bare.json` is `{}` **on purpose** — the
emptiness is the proof, not a config to fill in. A/B behavior is tested with
`Codex --safe-mode --system-prompt "" --tools "" --setting-sources ""
--strict-mcp-config --disable-slash-commands --settings .Codex/settings.bare.json`,
then dialing single "knobs" back on (`--append-system-prompt`, `--allowedTools`,
`--mcp-config`, `--permission-mode`, …). Full table in `.docs/what-is-a-harness.md`.

## Toolchain & commands

Environment is declared in `mise.toml` (node 26, bun 1.3.14, python 3.14, uv).

```sh
mise trust && mise install     # fresh clone setup
mise run check                 # runs test + test:py (see caveats below)
```

**Test suites (run these directly — the mise wrappers have gaps):**

```sh
# Python validators (.scripts/) — the real Python test suite, ~25 tests.
# NOTE: `mise run test:py` points at scripts/ (only match-lessons.py, no tests);
# the actual validator tests live in .scripts/.
python3 -m unittest discover -s .scripts -p 'test_*.py'

# skoghooks plugin hook smoke test — pipes every fixture through every wired
# hook; every hook must exit 0.
uv run marketplace/scripts/test_hooks.py

# TS hooks (.Codex/hooks/) have their own package.json:
cd .Codex/hooks && npm install && npm run check   # tsc --noEmit
```

`mise run test` (`node --test`) resolves to **0 tests** from the root — node's
default globber skips the hidden `.Codex/` dir where the `.test.js` files live
(`.Codex/tests/brainstorm-server/`). Run those with an explicit path if needed.

**Skill / doc validators** (`.scripts/`, each Python validator has a colocated
`test_*.py`):

```sh
python3 .scripts/validate_skill_quality.py
python3 .scripts/check_skill_language.py
python3 .scripts/check_reference_neutrality.py   # enforces public-surface neutrality
./.scripts/check-skills.sh                         # frontmatter structure of all skills
```

**Plugin validation:**

```sh
Codex plugin validate ./marketplace/plugins/skoghooks
Codex plugin validate ./marketplace                    # the marketplace itself
Codex --plugin-dir ./marketplace/plugins/skoghooks     # test locally, no install
```

## Repository map

| Path | Purpose |
|---|---|
| `.docs/` | Harness concept + pattern language (`what-is-a-harness.md`, `harness/`, `archive/`). The design source of truth. |
| `marketplace/` | Codex plugin marketplace. Has its own `AGENTS.md` + `AGENTS.md` — read them before touching plugins. |
| `marketplace/plugins/` | `skoghooks` (13-event hook reference impl), `skogharness`, `skogix-core-original`, `skogix-hooks`. |
| `.Codex/` | The **active** local harness config: `settings.json` (wires hooks), `skills/`, `hooks/` (TS), `agents/`, `commands/`, `tests/`. |
| `.scripts/` | Validation & maintenance domain (skill quality, reference neutrality, router/plugin-metadata/profile validators). See `.scripts/AGENTS.md`. |
| `scripts/` | `match-lessons.py`. |
| `.skogix/` | JSON `schemas/` (agent, skill, router, lesson, workflow, …) and `todo/gsd-planning/` planning workspace. |
| `.agents/`, `.codex/` | Cross-tool mirrors (codex cli is the "beta tester" for harness features). |
| `AGENTS.md`, `SKOGAI.md`, `AGENTS.md` | Live agent-instruction router files — must stay at their paths (`.docs/README.md`, "Not moved here"). |

## Two distinct hook systems (don't conflate them)

- **skoghooks plugin** (`marketplace/plugins/skoghooks/scripts/*.py`): the 13
  lifecycle hooks, Python + inline PEP 723 metadata (`#!/usr/bin/env -S uv run
  --script`), wired into `.Codex/settings.json` via `$CLAUDE_PROJECT_DIR/...`.
  Add hooks with the `/new-hook` skill or `scripts/new_hook.py`. Every hook must
  exit 0; exit 2 only to deliberately block. Runtime logs go to
  `<tmp>/skoghooks/<session_id>/`, never into the repo. Full detail:
  `marketplace/AGENTS.md`.
- **TS hook toolkit** (`.Codex/hooks/`): TypeScript hooks for skill
  auto-activation, session-doc updating, and `tsc` checks — its own
  `package.json`, run via `tsx`. Independent of the plugin above.

## Conventions

- **Router pattern.** `AGENTS.md` → `@SKOGAI.md`; docs use `<routes>` blocks with
  `@path` links. Preserve this shape (and the YAML frontmatter) when editing
  router files rather than inlining content.
- **Validators are policy.** `check_reference_neutrality.py` and
  `check_skill_language.py` encode distribution policy for the public surface —
  don't broaden their allowlists just to make a check pass.
- **New Python validator ⇒ colocated `test_<name>.py`** in `.scripts/`, using
  `unittest` + temp dirs + dynamic sibling-module loading (not package imports).
  `validate_router.py` is the one pre-existing exception.
- **Runtime artifacts are gitignored:** `.Codex/data/sessions`,
  `.Codex/worktrees`, `/tmp`, `.skogai/config/backups`. Don't treat them as
  committed state.
