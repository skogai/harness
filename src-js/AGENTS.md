# CORE RUNTIME GUIDANCE

## OVERVIEW

`src-js/` is the ESM programmatic API and harness synchronization implementation. `index.js` is the public export surface; commands materialize or reconcile agent-specific state.

## STRUCTURE

```text
src-js/
├── commands/  # init, add, sync, status, harness-init workflows
├── utils/     # guarded copy, managed blocks, security, TOON setup
├── manifest.js # skogai.json load/validate/resolve/save
├── mcps.js     # MCP validation and target payloads
├── agents.js   # target parsing and labels
├── profiles.js # shipped skills and profiles
└── index.js    # public named exports
```

## WHERE TO LOOK

| Change | Start here |
|---|---|
| Public API | `index.js`; export only intended stable entry points. |
| Installation | `commands/init.js`; installation ends in synchronization. |
| Manifest mutation | `commands/add.js`, then `manifest.js` and `commands/sync.js`. |
| Target drift | `commands/status.js`, `commands/sync.js`. |
| Copying / paths | `utils/copy.js`, `utils/security.js`. |
| MCP shape | `mcps.js` and `../schemas/manifest.schema.json`. |

## CONVENTIONS

- Use ESM with explicit `.js` relative imports and named exports.
- Validate input at boundaries and preserve the existing error wording/style.
- Keep target-specific behavior in command/sync layers; keep file/path primitives in `utils/`.
- Preserve conservative copy semantics: no symlink traversal and no implicit overwrite.

## ANTI-PATTERNS

- Do not bypass manifest validation or unknown-profile rejection.
- Do not accept an MCP entry containing both `command` and `url`, or a non-HTTPS remote URL.
- Do not overwrite `.claude/settings.json`; sync deliberately treats it as user-owned.
- Do not add an export to `index.js` merely for internal reuse; import the owning module directly.

## VALIDATION

```bash
bun run test
bun run test:security
```
