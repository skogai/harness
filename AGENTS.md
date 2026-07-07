# Repository Guidelines

## Project Structure & Module Organization

This repository is a Node.js ESM CLI package for `skogharness`. Runtime source lives in `src/`, with command handlers in `src/commands/` and shared helpers in `src/utils/`. The executable entry point is `bin/cli.js`, exposed as both `skogharness` and `harness`. Tests live in `test/` and use `*.test.js` naming. Agent and plugin templates are under `templates/`, with plugin metadata in `.claude-plugin/`. Keep generated dependencies in `node_modules/` out of commits.

## Build, Test, and Development Commands

- `bun install`: install dependencies from `bun.lock`.
- `bun run lint`: run ESLint across `src/`, `test/`, `bin/`, and template utilities.
- `bun test` or `npm test`: run the Node test suite via `node --test`.
- `bun run test:security`: run focused security-related tests in `test/*.test.js`.
- `bun run install:global`: run `scripts/install-global.sh` for a local global install.
- `node bin/cli.js status .`: exercise the CLI against the current repo during development.

## Coding Style & Naming Conventions

Use modern JavaScript modules with explicit `.js` imports. Follow the existing style: two-space indentation, single quotes, semicolons, and named exports for public helpers. CLI commands should live in `src/commands/<name>.js`; reusable logic should go in `src/utils/` or the relevant top-level module. ESLint enforces recommended JavaScript rules and permits unused function arguments only when prefixed with `_`.

## Testing Guidelines

Use the built-in `node:test` runner and `node:assert/strict`. Place tests in `test/` with descriptive names such as `manifest-sync.test.js` or `security-hardening.test.js`. Prefer temporary directories from `node:fs/promises` for filesystem tests, and register cleanup with `t.after()`. Add or update tests whenever behavior changes in manifest parsing, syncing, CLI commands, security checks, or template output.

## Commit & Pull Request Guidelines

Recent history uses short imperative subjects, often with Conventional Commit prefixes such as `feat: add harness creator skill`; keep that format for new work. Keep commits focused and avoid mixing template, CLI, and unrelated cleanup changes. Pull requests should describe the user-visible change, list validation commands run, link related issues when available, and include screenshots or terminal output only when the CLI behavior or generated files are easier to review visually.

## Security & Configuration Tips

Do not commit real tokens, local agent secrets, or generated user config. When adding MCP or environment handling, prefer placeholder variables such as `${GITHUB_PERSONAL_ACCESS_TOKEN}` and update `.env.example` behavior through managed sync code.
