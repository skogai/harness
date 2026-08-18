# Feature Specification: Truthfulness Rebaseline

**Feature Branch**: `001-truthfulness-rebaseline`

**Created**: 2026-08-18

**Status**: Draft

**Input**: User description: "Formalize the scope of the existing planning draft at
todo/drafts/post-prune-truthfulness-rebaseline.md (status: awaiting-approval) as the first
spec-kit feature spec: components 1-4 of its topology ledger (live-entrypoint-truth,
planning-provenance, current-decision-state, repository-validation-gate), adapted to the
current tracked tree. Component 5 (CLI/lifecycle restoration) stays explicitly deferred and
owner-pending, out of scope for this spec."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trust the routing and reference docs (Priority: P1)

An agent or maintainer opens `CLAUDE.md`, `SKOGAI.md`, or a file under `.docs/` to find where
something lives or how something works, follows a referenced path, and finds that the path
exists and matches what the doc says. Today at least one documented, linked path
(`.claude/settings.bare.json`, described in `.docs/what-is-a-harness.md` as the pinned
zero-config diff baseline) does not exist in the tracked tree, so following it silently fails
or misleads.

**Why this priority**: this is the most immediate, currently-observable falsehood in the
repo's own front door. Every other rebaseline effort depends on the router files being
trustworthy first.

**Independent Test**: can be fully tested by walking every `@path` reference and inline file
link in `CLAUDE.md`, `SKOGAI.md`, and `.docs/**` and confirming each resolves to a tracked,
existing file — independent of the validation-gate or planning-provenance work.

**Acceptance Scenarios**:

1. **Given** `.docs/what-is-a-harness.md` links to `.claude/settings.bare.json` as the pinned
   bare baseline, **When** a reader or automated check resolves that path, **Then** the file
   exists in the tracked tree and its content matches what the doc claims (`{}`).
2. **Given** any `<routes>`/`@path` entry in `CLAUDE.md` or `SKOGAI.md`, **When** the path is
   resolved against the current tracked tree, **Then** it points at a file or directory that
   actually exists (no route to a deleted, renamed, or never-committed path).

---

### User Story 2 - Trust the default check command (Priority: P2)

A maintainer or agent runs the repository's documented default check command before
considering a change done. The command reports success or failure, and that report is true:
success means real checks ran and passed; failure means a real problem was found. Today
`mise run check` can report success (exit 0) while running zero Node tests and while its
Python leg points at a directory containing no test files at all — a false-green result.

**Why this priority**: without a trustworthy pass/fail signal, every other truthfulness fix
in this spec can silently regress later with no one noticing. This is the mechanism that
keeps User Story 1 (and future changes) honest going forward.

**Independent Test**: can be fully tested by intentionally introducing a known structural
defect (e.g., a route pointing at a deleted file, or a documented command pointing at a
directory with zero matching test files) and confirming the default check command exits
non-zero — independent of the entrypoint-truth content fixes themselves.

**Acceptance Scenarios**:

1. **Given** the repository in its current, structurally sound state, **When** the default
   check command runs, **Then** it exits zero only after having actually evaluated a nonzero
   number of real checks/candidates (not a vacuous pass).
2. **Given** a deliberately broken fixture (a referenced path that does not exist, or a
   documented command that would run zero tests), **When** the default check command runs
   against that fixture, **Then** it exits non-zero and reports which check failed and why.
3. **Given** the current, real `mise run check` composition, **When** it is evaluated against
   this new gate's own fail-closed criteria, **Then** the gap already documented in
   `CLAUDE.md` (zero-Node-test leg, Python leg pointed at the wrong directory) is detectable
   by the gate rather than silently passing.

---

### User Story 3 - Know what's historical vs. current in planning (Priority: P3)

A maintainer or agent looking for "what's the current plan" opens a planning directory and
can immediately tell, without reading git history or comparing byte-for-byte content, whether
what they're looking at is the live, authoritative plan or a preserved historical artifact
that no longer describes the current tracked tree.

**Why this priority**: prevents an agent from silently treating stale planning (e.g. content
in `.skogix/todo/gsd-planning/` that assumes deleted CLI/runtime paths) as current instruction,
without deleting or rewriting anything that might still hold useful intent.

**Independent Test**: can be fully tested by locating every existing planning tree that
references now-absent surfaces and confirming each carries an explicit, visible
historical/non-authoritative label — independent of the other three stories.

**Acceptance Scenarios**:

1. **Given** a planning tree whose content assumes paths or surfaces that no longer exist in
   the tracked tree, **When** a maintainer or agent opens that tree, **Then** it is
   unambiguously and immediately marked historical/non-authoritative, without any change to
   its substantive content.
2. **Given** the current live planning surface, **When** a maintainer or agent looks for it,
   **Then** it is distinguishable at a glance from the historical trees (no ambiguity about
   which one to trust).

---

### User Story 4 - Know what's decided vs. still owner-pending (Priority: P4)

A maintainer or agent wants to know, in one place, which repo-shape decisions are settled and
which are explicitly still waiting on the owner (skogix/emil) — most notably, whether the
deleted CLI/lifecycle/runtime surface is coming back — without having to reconstruct that from
scattered commit history or stale planning docs.

**Why this priority**: lowest urgency of the four stories (it's a documentation/record
artifact, not a truth-integrity fix), but it closes the loop the other three stories open —
it's where "deferred, not rejected" gets written down so nobody re-litigates or silently
assumes an answer.

**Independent Test**: can be fully tested by reading the one current-decision-state record and
confirming it correctly separates "settled" from "owner-pending" without taking a position on
any owner-pending item — independent of the other three stories.

**Acceptance Scenarios**:

1. **Given** the current-decision-state record, **When** a reader checks whether CLI/lifecycle
   restoration is decided, **Then** the record states it is explicitly owner-pending, not
   settled either way.
2. **Given** a decision that genuinely has been settled (e.g., "the tracked tree, not a
   restored CLI surface, is the current execution baseline"), **When** a reader checks the
   record, **Then** that decision is recorded as settled with enough context to not need to
   ask again.

### Edge Cases

- What happens when a route/reference points at a directory rather than a file (e.g.
  `marketplace/`)? The existence check must still apply — a directory reference must resolve
  to an existing directory.
- What happens when a documented command's target directory exists but currently contains
  zero matching test files (the live `test:py`/`scripts/` situation)? The gate must treat this
  as a failure, not silently report "ran 0 tests, exit 0" as success.
- What happens when new historical planning content is added later (a future prune)? The
  provenance-labeling mechanism established here must be reusable, not a one-time manual fix.
- What happens if a route legitimately needs to point outside the tracked repo (e.g. a global
  path)? Out of scope for "exists in tracked tree" checks — flagged separately as a
  global-state dependency, which the validation gate must also reject per its fail-closed
  requirement (see Scope OUT below and FR-006).
- What happens when the owner later resolves the CLI/lifecycle-restoration question? The
  current-decision-state record must be a living document that gets updated at that point, not
  re-created from scratch.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every path referenced via `<routes>`/`@path` links or inline file references in
  `CLAUDE.md`, `SKOGAI.md`, and `.docs/**` MUST resolve to a file or directory that exists in
  the current tracked tree.
- **FR-002**: `.claude/settings.bare.json` MUST exist in the tracked tree and MUST contain
  exactly `{}`, matching what `.docs/what-is-a-harness.md` already documents it to be.
- **FR-003**: The repository MUST provide one repo-local, fail-closed structural validation
  check that detects: (a) a documented/routed reference to a path that does not exist in the
  tracked tree, and (b) a documented command whose target evaluates zero real
  checks/tests/candidates.
- **FR-004**: The validation check from FR-003 MUST be wired into the repository's default
  check surface (the command described in `CLAUDE.md` as `mise run check` or its direct
  dependents) so that a normal "run the checks" invocation exercises it.
- **FR-005**: The validation check MUST fail (non-zero exit) on a run that would otherwise
  report success with zero checked candidates — a "vacuous pass" MUST NOT be treated as a
  passing run.
- **FR-006**: The validation check MUST NOT depend on state outside the tracked repository
  (e.g. global user config under `~/.claude`, machine-local paths, or generated/ignored files)
  to determine pass/fail.
- **FR-007**: The repository MUST include both a positive fixture (demonstrating the gate
  passes on a structurally sound tree) and at least one negative fixture per failure mode in
  FR-003 (demonstrating the gate fails closed), so the gate's own correctness is verifiable.
- **FR-008**: Existing planning trees whose content no longer describes the current tracked
  tree (at minimum `.skogix/todo/gsd-planning/` and any other planning copy found to reference
  absent surfaces) MUST be labeled historical/non-authoritative, without deleting or rewriting
  their substantive content.
- **FR-009**: The repository MUST provide exactly one current, live decision-state record that
  states which repo-shape decisions are settled and which remain explicitly owner-pending.
- **FR-010**: The current-decision-state record MUST record CLI/lifecycle/runtime restoration
  as owner-pending — this spec MUST NOT settle that question either way.
- **FR-011**: The current-decision-state record and the historical-planning labels from FR-008
  MUST be discoverable from the repository's router files (`CLAUDE.md`/`SKOGAI.md`), so an
  agent following normal routing conventions reaches them without being told where to look.

### Key Entities

- **Documented Reference**: a path named in a router file (`CLAUDE.md`, `SKOGAI.md`) or a
  `.docs/**` doc, or a command target named in `mise.toml`/`CLAUDE.md`'s command list; has an
  existence state (exists / missing) and, for commands, a candidate count (real checks it
  would run).
- **Planning Artifact**: a document or tree under a planning location (e.g.
  `todo/drafts/`, `.skogix/todo/gsd-planning/`); has a provenance status of either current/live
  or historical/non-authoritative, plus its unmodified original content.
- **Decision-State Record**: the single live document listing settled decisions (with
  rationale) and owner-pending decisions (explicitly not yet decided), most notably the
  CLI/lifecycle/runtime restoration question.
- **Validation Gate**: the repo-local structural check itself; has a set of evaluated
  candidates per run, a pass/fail result per candidate, and an overall fail-closed verdict that
  cannot be "success" when the candidate count is zero.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of paths referenced by `CLAUDE.md`, `SKOGAI.md`, and `.docs/**` resolve to
  files or directories that exist in the tracked tree, confirmed by an automated check with no
  manual review step required.
- **SC-002**: The default repository check command exits non-zero on 100% of intentionally
  introduced structural defects (broken route, zero-candidate documented command), confirmed
  by the negative fixtures required in FR-007.
- **SC-003**: A person unfamiliar with the repo's recent history can, within one file read,
  correctly identify which of the two (or more) planning trees is current and which are
  historical, with zero ambiguity.
- **SC-004**: A person unfamiliar with the repo's recent history can, within one file read,
  correctly state whether CLI/lifecycle restoration has been decided, without consulting git
  log or prior planning drafts.
- **SC-005**: Re-running the default check command on an untouched, structurally sound
  repository continues to exit zero (no false positives introduced by the new gate).

## Assumptions

- The current tracked tree (this branch's checkout) is treated as the execution baseline for
  "exists" checks — not any deleted/pruned historical state and not a hypothetical restored
  CLI surface.
- "Historical planning trees" in scope for FR-008 are the ones already identified as
  referencing absent surfaces (at minimum `.skogix/todo/gsd-planning/`); if other stale
  planning copies are found during implementation, the same labeling treatment applies to them
  without requiring a new spec.
- The validation gate added here is additive: it complements, and does not replace or modify,
  the existing `.scripts/` validators, `marketplace/scripts/test_hooks.py`, or the TS hook
  toolkit's own `tsc` check.
- "Default check surface" refers to the `mise run check` task as currently documented in
  `CLAUDE.md`; if that command is renamed or restructured independently of this feature, the
  wiring requirement (FR-004) follows the renamed default, not the literal string `mise run
  check`.
- Resolving the CLI/lifecycle/runtime restoration question itself, and any work to restore
  such a surface, is out of scope (component 5 of the source planning draft, left
  deferred/owner-pending) — this spec only records that it is undecided, per FR-010.
- "Owner" in FR-009/FR-010 refers to the repository owner (skogix/emil); an agent completing
  this spec's requirements does not thereby gain authority to answer the owner-pending
  question.
