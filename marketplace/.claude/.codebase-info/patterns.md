# Patterns & Conventions

*Last Updated: 2026-09-15*

## Shared across hook-bearing plugins (skoghooks, skogharness, skogix-hooks)

- **Fail-open by default, fail-closed only when deliberate.** Every hook script catches its own
  exceptions and exits 0; a non-zero (specifically exit 2) exit is reserved for intentional blocking
  and used sparingly. `plugins/skoghooks/CLAUDE.md`'s hook pattern states this explicitly ("Never
  crash: all hooks catch all exceptions and exit 0"); `plugins/skogix-hooks/hooks/pre-tool-use.sh` is
  the clearest live example of the fail-closed exception (regex-based guardrail, exit 2 to block).
- **Standalone, dependency-manifest-free scripts.** No plugin has a shared `package.json`/
  `pyproject.toml`. Python hooks use PEP 723 inline `uv run --script` headers; Node hooks use only
  stdlib; jq transforms are zero-dependency by design. See
  [tech-landscape.md](tech-landscape.md#cross-cutting-observation) — likely a deliberate house rule,
  confirm before adding a shared manifest to any plugin tree.
- **Session-scoped runtime state, never committed.** Logs/backups/transcripts write to a tmp dir keyed
  by session id (`$CLAUDE_CODE_TMPDIR/<plugin>/<session_id>/` or `/tmp/...`), not into the repo. Don't
  expect a `logs/` directory to exist or be meaningful in git history.
- **`AGENTS.md` as a per-directory router.** `plugins/skogix-hooks/` puts an `AGENTS.md` in nearly
  every subdirectory (plugin root, `hooks/`, `skills/`) with explicit "WHERE TO LOOK" tables and
  "ANTI-PATTERNS" sections — a stronger version of the repo-root `AGENTS.md`/`CLAUDE.md` router
  pattern. `plugins/skogix-core-original/` formalizes this same idea into a whole meta-framework
  (routing files + references + workflows + templates + schemas).

## `plugins/skoghooks/`-specific

- Block a tool call: print reason to stderr, `sys.exit(2)`. Inject context: print
  `{"hookSpecificOutput": {"additionalContext": "..."}}` and exit 0. (Documented in root CLAUDE.md,
  confirmed accurate.)
- The `rm -rf`/`.env`-access blocking helpers in `pre_tool_use.py`
  (`is_dangerous_rm_command()`, `is_env_file_access()`) are **present but unused** — disabled due to
  false positives (e.g. `git rm -rf`). This plugin logs only; contrast with `skogix-hooks`, whose
  equivalent guardrail is live.

## `plugins/skogix-hooks/`-specific

- **90%+ test coverage mandate including falsy-value edge cases** (`null`, `false`, `0`, `""`) for
  every `skogai-jq` transform — stated in `AGENTS.md`, enforced via each transform's own `test.sh`
  plus a `test-all.sh` aggregator.
- Transforms are deliberately tiny (5-40 lines), schema-first, and composable via Unix pipes —
  optimized explicitly "for AI agent discoverability," per the plugin's own docs.
- Incubator convention: hooks/skills here are meant to be promoted to standalone plugins once mature
  (per `AGENTS.md`) — don't treat code here as a stable public API.

## `plugins/skogharness/`-specific

- `PLUGIN_SCHEMA_NOTES.md` documents undocumented `plugin.json` validator quirks: manifest component
  fields must be arrays, and an `"agents"` field must **not** appear in `plugin.json` (breaks
  validation) even though the plugin ships 67 agent definitions — they're auto-discovered some other
  way, not declared in the manifest. Read this file before touching `plugin.json` in any plugin here.
- Every `hooks.json` command is a one-line `node -e "..."` bootstrap resolving `CLAUDE_PLUGIN_ROOT`
  with fallback scans of `~/.claude/plugins/cache/{ecc,everything-claude-code}/...` — built to survive
  being installed under either the "ecc" or "skogharness" name/path. If you're renaming or moving
  files, check these fallback paths don't silently break.

## Cross-repo caution

Root `CLAUDE.md`/`AGENTS.md`/`README.md` describe `plugins/skoghooks/` only. **Do not extrapolate
their conventions onto `skogharness`, `skogix-hooks`, or `skogix-core-original`** — each has different
exit-code conventions, different manifest requirements, and (for skogharness/skogix-hooks) different
lifecycle-event schemas entirely.
