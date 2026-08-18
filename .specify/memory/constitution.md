<!--
Sync Impact Report
- Version change: (none) → 1.0.0 (initial ratification)
- Modified principles: n/a (first adoption)
- Added sections:
  - Core Principles: I. Bare-Baseline A/B Attribution, II. Plane-Based Harness Design,
    III. Meta-Repo Scope Discipline, IV. Router Pattern Integrity, V. Fail-Closed Validation
  - Documented Surfaces & Structure
  - Development Workflow & Quality Gates
  - Governance
- Removed sections: n/a
- Templates requiring follow-up: none — plan/spec/tasks templates consume this file at
  runtime via the resolver and contain no hardcoded principle references to update.
- Deferred placeholders: none. RATIFICATION_DATE set to the date of this initial adoption
  since no prior ratified constitution exists.
-->

# skogai-harness Constitution

## Core Principles

### I. Bare-Baseline A/B Attribution
Every harness addition (system prompt, tools, settings, mcp, skills, hooks, memory) MUST be
justified by an observed behavior delta against the literal zero-configuration baseline, not
by intuition or convention. The baseline is `.claude/settings.bare.json`, which MUST remain
`{}` — the emptiness is the pinned proof that zero settings are required, not a config to
fill in. Attribution is performed by invoking `claude --safe-mode --system-prompt ""
--tools "" --setting-sources "" --strict-mcp-config --disable-slash-commands --settings
.claude/settings.bare.json` as the fixed point, then dialing individual "knobs" (e.g.
`--append-system-prompt`, `--allowedTools`, `--mcp-config`, `--permission-mode`) back on one
at a time. A behavior change MUST be attributable to a single isolated knob before it is
accepted as evidence for a harness change; changes justified only by "the whole stack
together" are not acceptable evidence.

**Rationale**: without a pinned, literal zero point, every claim of "this hook/prompt/skill
improves behavior" is unfalsifiable — the bare baseline exists specifically to make harness
claims testable.

### II. Plane-Based Harness Design
Every harness change MUST be describable in terms of the planes defined in
`.docs/what-is-a-harness.md`: request assembly, turn loop, tool plane, memory plane, recovery
plane, human control, extension plane. Design docs and blueprints MUST be organized per-plane
(one section per plane, per the blueprint template) rather than as ad hoc feature lists. A
change that cannot be mapped to a plane is either out of scope for this repo or indicates a
missing plane in the framework that must be named explicitly before the change proceeds.

**Rationale**: the planes exist to stop harness work from collapsing into "a prompt with a
tool list" or "a loop with no governance" — the weak states the framework was written to
avoid.

### III. Meta-Repo Scope Discipline
skogai-harness is not an application — it produces (1) a blueprint/pattern framework under
`.docs/` and (2) the concrete, testable artifacts of that framework: a Claude Code plugin
marketplace, skills, hooks, and validators under `marketplace/` and `.claude/`. Work that
does not serve one of these two outputs (product features, unrelated app-level code,
business logic unconnected to harness design or testing) is out of scope and MUST NOT be
accreted into this repo. When in doubt whether a change belongs, it MUST map to a
repository-map entry in `CLAUDE.md` or be added there explicitly as a new, justified surface.

**Rationale**: a meta-repo that builds harnesses accrues scope creep easily if "useful code"
is allowed in without a documented purpose — scope discipline keeps the repo legible as a
blueprint generator, not a growing application.

### IV. Router Pattern Integrity
`CLAUDE.md` → `@SKOGAI.md` and `<routes>` blocks with `@path` links are the live
agent-instruction routing mechanism for this repo. Router files (`CLAUDE.md`, `SKOGAI.md`,
`AGENTS.md` where present) MUST stay at their pinned paths, MUST preserve the router shape
(YAML frontmatter, `<routes>` blocks) when edited rather than being inlined or restructured,
and MUST describe only tracked, currently-existing surfaces. A route pointing at a deleted,
renamed, or never-committed path is a defect and MUST be corrected or removed, not left as
aspirational documentation.

**Rationale**: routers are read by agents as ground truth for where to look; a stale route
silently misdirects every agent that trusts it, which is worse than no route at all.

### V. Fail-Closed Validation
Checks that encode distribution or neutrality policy for the public surface (e.g.
`check_reference_neutrality.py`, `check_skill_language.py`) MUST NOT have their allowlists
broadened merely to make a failing check pass — the check failing is a signal to fix the
content, not the gate. Any validation gate added to this repository (skill/doc validators,
structural checks, CI-equivalent tasks) MUST be fail-closed: it MUST reject zero-test or
zero-candidate runs, vacuous passes, warnings/skips treated as success, stale routes, and
dependencies on global/out-of-repo state (e.g. `~/.claude`, machine-local paths). A gate that
can report success without checking anything real (a false-green gate) is treated as a
defect with the same priority as a failing test.

**Rationale**: validators are the repo's only automated defense of its own documented
policies; a gate that can go green for the wrong reasons is worse than no gate, because it
manufactures false confidence.

## Documented Surfaces & Structure

The repository map in `CLAUDE.md` is the authoritative index of top-level surfaces
(`.docs/`, `marketplace/`, `.claude/`, `.scripts/`, `scripts/`, `.skogix/`, `.agents/`,
`.codex/`). New top-level directories or repurposed existing ones MUST be reflected there.
`marketplace/` maintains its own `CLAUDE.md` and `AGENTS.md` for plugin-specific guidance and
MUST be read before changes inside it. This repo maintains two distinct hook systems that
MUST NOT be conflated: the `skoghooks` plugin (`marketplace/plugins/skoghooks/scripts/*.py`,
the 13-event lifecycle hooks wired via `.claude/settings.json`) and the TS hook toolkit
(`.claude/hooks/`, independent, its own `package.json`/`tsc` pipeline). Changes to one MUST
NOT silently assume behavior of the other.

## Development Workflow & Quality Gates

Test suites MUST be run directly rather than solely through `mise run check`, since the mise
wrapper is documented to have gaps (`mise run test` resolves to 0 tests from the root because
node's default globber skips `.claude/`; `mise run test:py` points at `scripts/`, not the
real validator suite in `.scripts/`). At minimum, before a change touching skills, hooks, or
validators is considered complete: `python3 -m unittest discover -s .scripts -p
'test_*.py'`, `uv run marketplace/scripts/test_hooks.py`, and (for TS hooks)
`cd .claude/hooks && npm run check` MUST pass. Any new Python validator under `.scripts/`
MUST ship with a colocated `test_<name>.py` using `unittest`, temp dirs, and dynamic
sibling-module loading, consistent with the existing suite (the one pre-existing exception is
`validate_router.py`). Plugin changes MUST be validated with `claude plugin validate` against
both the specific plugin and the marketplace as a whole before being considered done.

## Governance

This constitution supersedes ad hoc convention where the two conflict; CLAUDE.md and
SKOGAI.md remain the operational routers for day-to-day agent instructions, but MUST NOT
contradict a ratified principle here without the amendment procedure below being followed.

**Amendment procedure**: amendments are proposed as edits to this file, ratified by explicit
approval, and take effect immediately on merge. Every amendment updates `Last Amended` to the
date of the change and appends or updates the Sync Impact Report comment at the top of this
file describing what changed and why.

**Versioning policy**: this file follows semantic versioning for governance documents —
MAJOR for backward-incompatible principle removals or redefinitions, MINOR for a new
principle or materially expanded guidance, PATCH for clarifications and non-semantic
wording fixes.

**Compliance review**: any change proposed against this repo (spec, plan, or direct edit)
MUST be checkable against the five Core Principles above. A reviewer (human or agent) who
cannot map a proposed harness change to a plane (Principle II), cannot state what behavior
delta justifies it (Principle I), or finds it adds scope outside `.docs/`/`marketplace/`/
`.claude/` (Principle III) MUST raise that as a blocking concern before the change proceeds.

**Version**: 1.0.0 | **Ratified**: 2026-08-18 | **Last Amended**: 2026-08-18
