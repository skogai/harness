# SCHEMA CONTRACT GUIDANCE

## OVERVIEW

`schemas/` holds JSON Schema Draft 2020-12 contracts for normalized documents, harness manifests, and supporting data. Schema changes are compatibility changes: update the layer that owns the invariant, not an arbitrary subtype.

## STRUCTURE

| Layer | Files |
|---|---|
| Shared primitives | `defs.schema.json`, `frontmatter.schema.json`, `document.schema.json` |
| Document types | `router`, `workflow`, `reference`, `template`, `script`, `lesson`, `pattern`, `decision`, `principle`, `skill` schemas |
| Runtime/data shapes | `manifest`, `agent`, `list`, `message`, `skogchat-message`, `transform` schemas |

## WHERE TO LOOK

| Change | Location |
|---|---|
| Shared field or enum | `defs.schema.json` first; follow references into dependent schemas. |
| Common document field | `frontmatter.schema.json` or `document.schema.json`. |
| One document kind | Its `*.schema.json` subtype. |
| `skogai.json` behavior | `manifest.schema.json` and `../src-js/manifest.js`. |
| Markdown schema validation | `../scripts/validate-schema.sh`, `../scripts/_validate_file.py`. |

## CONVENTIONS

- Preserve the `$id` / Draft 2020-12 convention and existing `$ref` layering.
- Keep reusable primitives in `defs.schema.json`; do not copy enum or pattern definitions into every subtype.
- Treat `list.schema.json` content as ordered and append-only.
- Check the validator mapping before adding a document type; `_validate_file.py` defines the active type-to-schema surface.

## ANTI-PATTERNS

- Do not assume every schema is currently runtime-consumed; document validators only map selected document types.
- Do not describe `type: skill` as fully wired: `skill` is not yet present in the shared `defs.type` enum.
- Do not add file-existence assumptions to manifest schema validation; structural validation does not prove referenced files exist.

## VALIDATION

```bash
./scripts/validate-schema.sh
```
