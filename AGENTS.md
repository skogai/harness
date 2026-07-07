# Repository Guidelines

## Project Structure & Module Organization

This repository is the `skogharness` CLI package. Runtime code lives in `src/`, with command implementations in `src/commands/` and shared helpers in `src/utils/`. The executable entry point is `bin/cli.js`. Tests live in `test/*.test.js` and use Node's built-in test runner.

Templates are part of the product. The canonical shared skill source is `templates/.claude/skills/`; Codex output is generated from that source and static Codex template files live under `templates/codex/`. Avoid hand-maintaining duplicated skill content across agent targets.

## Build, Test, and Development Commands

- `bun install`: install dependencies using the pinned package manager.
- `npm test`: run all Node test files with `node --test`.
- `npm run test:security`: run the current security-focused test suite pattern.
- `npm run lint`: lint `src/`, `test/`, `bin/`, and Claude utility templates.
- `node bin/cli.js --agent codex`: smoke-test local CLI output for Codex.

For installer changes, test real output in a temporary directory, for example:

```bash
tmpdir="$(mktemp -d)"
cd "$tmpdir"
node /home/skogix/harness/bin/cli.js --agent all
find . -maxdepth 3 -type f | sort
```

## Coding Style & Naming Conventions

Use ESM JavaScript (`import`/`export`) and keep modules focused by command or utility responsibility. Follow the existing two-space indentation style. File names are lowercase with hyphens where needed, such as `managed-block.js`. Tests should be named `*.test.js`.

ESLint uses `@eslint/js` recommended rules and treats unused variables as errors, except arguments prefixed with `_`.

## Testing Guidelines

Add focused regression tests in `test/` for CLI behavior, manifest sync, template output, security hardening, and installer changes. When generated files or target behavior changes, include coverage that exercises real install output instead of only helper-level behavior.

## Commit & Pull Request Guidelines

Recent history uses concise imperative commit subjects, for example `Remove Cursor support and deprecate unused infrastructure` and `Simplify marketplace config to toon-formatter only`. Keep PRs scoped, describe user-facing CLI or template changes, and mention any generated-output or installer smoke checks performed.

## Security & Configuration Tips

Never commit real secret values. Generated configuration should reference secrets as `${VAR}` and preserve user-managed config outside harness-managed blocks.
