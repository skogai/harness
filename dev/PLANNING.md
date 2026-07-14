# Skogharness Basic Structure Plan

## Purpose

Mirror the useful workflow shape from `.example/superclaude/` into `skogharness/` without building the full system yet.

This first slice is intentionally small: persistent dev docs, one example agent, one example command, and one basic hook definition.

## Source Model

- `.example/` is inspiration only.
- `.example/superclaude/` is the reference for package shape and workflow categories.
- `skogharness/` is the target implementation area.

## Phase 1 Scope

Create the smallest useful structure:

- `dev/PLANNING.md` for plan and scope.
- `dev/TASK.md` for the active checklist.
- `dev/KNOWLEDGE.md` for decisions and lessons.
- `src/skogharness/agents/example.md` as a minimal agent example.
- `src/skogharness/commands/example.md` as a minimal command example.
- `src/skogharness/hooks/README.md` and `hooks.json` as a basic hook example.

## Out Of Scope

- No installer changes.
- No tests in this phase.
- No MCP setup.
- No runtime hook scripts.
- No root repository entrypoint changes.
- No `harness-creator` changes.
- No contributing, versioning, doctor, drift detection, or release work.

## Acceptance Criteria

- The basic files exist under `skogharness/`.
- The examples are clearly marked as examples.
- The hook config is documentation/example material, not claimed as active runtime behavior.
- Future work can build tests and installer behavior around this structure later.

## Phase 2 Scope

Make the basic framework installable and testable without expanding into runtime behavior.

This slice turns the existing category directories into an automated installer surface driven by the repo's `mise` tasks. It keeps `.example/superclaude/` as reference material only and keeps `skogharness/` as the implementation target.

Create the smallest useful automated installer:

- Keep `dev/PLANNING.md`, `dev/TASK.md`, and `dev/KNOWLEDGE.md` as the persistent planning structure.
- Install supported source categories from `src/skogharness/<category>/` into a target `.claude/<category>/` directory.
- Preserve the existing `skogharness install skills` command while adding the same copy behavior for the other basic categories.
- Drive verification through the existing `mise run test:skogharness` task.
- Keep category files clearly marked as examples unless they are real skills.

## Phase 2 Out Of Scope

- No runtime hook scripts.
- No MCP server setup.
- No root repository entrypoint changes.
- No `harness-creator` changes.
- No manifest, sync, status, drift detection, doctor, or release workflow.

## Phase 2 Acceptance Criteria

- Installer tests cover skill and non-skill category installation.
- CLI dry-run and install paths can be exercised through the Python package command.
- `mise run test:skogharness` passes.
- README and category docs describe the basic installer without claiming active runtime behavior.
