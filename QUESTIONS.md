# Open questions — harness state cleanup

Context: working through the "known drift" items in this repo. The
unambiguous, one-correct-answer bugs are already fixed, and a round of
explicit simplification instructions (remove speckit, minimal CLAUDE.md,
AGENTS.md as a symlink) has also been applied — see "Already done" at the
bottom. What's left below still needs a decision.

## 1. `validate_router.py` runs now, but fails on every real router file

Fixing its schema path (bug fix, already done) unblocked it — and it
immediately reports `CLAUDE.md`/`SKOGAI.md` as **FAIL**. Not because of the
path bug: `router.schema.json` defines a router as a "decision hub" with
`description` + `routing` sections (named branches, each a condition →
destination). The actual convention used everywhere in this repo — now more
so than ever, since `CLAUDE.md` is down to a bare `<routes>` block — is a
plain `- @path` bullet list. These are two incompatible ideas of "router."

- Should `router.schema.json` be rewritten to match the `<routes>`/`@path`
  convention actually in use?
- Or should router files grow real `description`/`routing` sections to match
  the schema?

I'd lean toward rewriting the schema to match the convention you're actively
using and just reinforced (CLAUDE.md/AGENTS.md as pure pointers), but didn't
want to change policy docs without you confirming.

## 2. `SKOGAI.md`'s `<routes>` block is an empty dead end

It's currently:
```
<routes>

-

</routes>
```
A bullet with nothing after it. This now matters more than before: `CLAUDE.md`
routes here, and `AGENTS.md` is a symlink to this exact file, so this is the
one real content file both entrypoints resolve to — and it currently has no
content and no working route. What should it contain / point at?

---

## Already done

**Pure bug fixes (verified):**
- Created `.claude/settings.bare.json` with `{}` — was referenced everywhere,
  didn't exist.
- `.scripts/check-skills.sh`: path derivation overshot by one directory level
  (`$SCRIPT_DIR/../..` → `$SCRIPT_DIR/..`). Verified: now exits 0 and finds
  the real skills directory.
- `.scripts/validate_router.py`: `SCHEMA_DIR` pointed at `templates/schemas/`
  (doesn't exist) instead of `.skogix/schemas/` (where `router.schema.json`
  actually lives). Verified: script now runs instead of crashing — see item 2
  above for what it found once unblocked.

**Per your explicit instructions this round:**
- Removed spec-kit fully: `.specify/` (constitution, templates, scripts,
  workflows), `specs/` (`001-truthfulness-rebaseline` and its checklist), and
  all ten `speckit-*` skill directories under both `.claude/skills/` and
  `.agents/skills/`.
- `CLAUDE.md` reduced to just frontmatter + a `<routes>` block pointing at
  `@SKOGAI.md` — no more prose/content.
- `AGENTS.md` replaced with a symlink to `SKOGAI.md` (`AGENTS.md ->
  SKOGAI.md`), so the two can no longer drift apart as separate files.
- Trimmed `mise.toml`'s `test`/`test:py`/`check` tasks entirely — they were
  built on the wrong premise that this root has tests to run. Confirmed: this
  dir is the meta/overview dev environment, not a shipped artifact; actual
  products and their tests live one level down (e.g. `marketplace/`). `mise`
  here is just tool-version pinning + the one real utility task
  (`install-skogcli`), used when needed rather than as a CI gate.
