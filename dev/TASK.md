# Skogharness Basic Structure Tasks

## Phase 1: Basic Files

- [x] Create `dev/PLANNING.md`.
- [x] Create `dev/TASK.md`.
- [x] Create `dev/KNOWLEDGE.md`.
- [x] Replace the placeholder agent example with a minimal real example.
- [x] Replace the placeholder command example with a minimal real example.
- [x] Add a basic hooks directory.
- [x] Add a basic hook example config.

## Not Started

- [x] Add tests around category installer behavior.
- [x] Add installer support for non-skill categories.
- [ ] Add real hook scripts.
- [ ] Add validation or doctor commands.

## Phase 2: Automated Basic Installer

- [x] Open Phase 2 scope in `dev/PLANNING.md`.
- [x] Add RED tests for generic category installation.
- [x] Preserve `skogharness install skills` behavior.
- [x] Add `skogharness install agents|commands|hooks|mcp|modes`.
- [x] Document `mise run test:skogharness` as the installer verification path.
- [x] Run final full `mise run test:skogharness` verification.
- [x] Exercise real CLI dry-run and install scenarios.

## Resume Notes

Continue with the automated basic installer only. Do not expand into runtime hooks, MCP setup, drift detection, doctor commands, or release workflow until this installer surface is stable and verified.
