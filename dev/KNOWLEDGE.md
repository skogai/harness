# Skogharness Basic Structure Knowledge

## Decisions

- `.example/` is reference material only.
- `skogharness/` is the implementation target equivalent to `.example/superclaude/`.
- Phase 1 is documentation and example shape only.
- The first hook is an example config, not a working automation path.
- Phase 2 uses `mise run test:skogharness` as the main verification command for the package installer.
- Non-skill categories are installable as copied example files, not active runtime behavior.

## Current Boundaries

- Keep this work inside `skogharness/`.
- Do not modify `harness-creator`.
- Installer and test behavior may cover the basic category framework now that Phase 1 exists.
- Do not add real runtime hooks, MCP server setup, drift detection, or doctor commands in the basic installer slice.

## Notes

- The `dev/` docs mirror the persistent context pattern from `.example/dev/README.md` in a simpler form.
- The initial agent, command, and hook files should be boring and explicit. Their job is to establish shape, not functionality.
- Installer behavior should remain plain copy with dry-run support and source-overlap protection. No manifest or managed-block tracking yet.
