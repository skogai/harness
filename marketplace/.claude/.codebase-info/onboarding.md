# Onboarding

*Last Updated: 2026-09-15*

Start with [plugins.md](plugins.md) — this repo has four unrelated plugin-shaped projects under
`plugins/`, and "the plugin" is ambiguous until you know which one a task concerns.

## Working on `plugins/skoghooks/` (the one registered in this repo's marketplace)

```shell
# Test locally without installing
claude --plugin-dir ./plugins/skoghooks

# Add this repo as a marketplace, then install
/plugin marketplace add ./
/plugin install skoghooks@skoghooks

# Validate
claude plugin validate ./plugins/skoghooks
claude plugin validate .

# Run every wired hook against its fixture, expect exit 0
uv run scripts/test_hooks.py

# Run one hook script directly
echo '{"session_id":"test","hook_event_name":"SessionStart"}' \
  | uv run plugins/skoghooks/scripts/session_start.py --load-context
```

Use the `/new-hook` skill (or `uv run scripts/new_hook.py <Event> <name> [--matcher ...] [--flags=...]`
by hand) to scaffold a new hook — see root `CLAUDE.md` for the full flag/event table.

## Working on `plugins/skogharness/`

It has its own `.claude-plugin/marketplace.json`, independent of the repo root's:

```shell
/plugin marketplace add ./plugins/skogharness
```

Read `plugins/skogharness/PLUGIN_SCHEMA_NOTES.md` before touching `plugin.json` — it documents
non-obvious validator rules (e.g. don't add an `"agents"` field). Read `plugins/skogharness/AGENTS.md`
first for the "Everything Claude Code" overview (67 agents, 92 commands, ~80+37 skills). No test
runner for the JS hook system; the only real test target is
`skills/skogai/continuous-learning-v2/scripts/instinct-cli.py` via
`test_parse_instinct.py` (plain `pytest`, no confirmed pytest config).

## Working on `plugins/skogix-hooks/` (`dot-core`)

No `.claude-plugin/plugin.json` — it's not installable as a Claude Code plugin as-is; it targets
Codex's 6-event hook schema via `.codex-plugin/plugin.json` and `hooks.json`. Read its `AGENTS.md`
first — it's explicitly an incubator, and every subdirectory has its own `AGENTS.md` router.

```shell
# Bats shell tests
bats tests/*.bats

# Python lesson-matcher tests
uvx pytest hooks/test_lesson_matcher.py -v

# A single skogai-jq transform's tests
bash skills/skogai-jq/<transform-dir>/test.sh
# Or all of them
bash skills/skogai-jq/test-all.sh   # if present — confirm path before relying on it
```

## Working on `plugins/skogix-core-original/` (`skogai-routing`)

Start at `SKILL.md`. This is a documentation/routing meta-framework, not runtime code — changes here
are about how routing files, workflows, references, templates, and schemas should be structured
across the SkogAI ecosystem, not about hook behavior. Validate a file against its schema with
`scripts/_validate_file.py` or `scripts/validate-schema.sh`.

## Cross-cutting gotchas worth knowing before you start

- Root `.todo/*.md` are memory-agent scratch notes (Serena-style `mem:*` files) summarizing the repo —
  useful for a fast orientation read, but not authoritative; this codebase map (`.claude/.codebase-info/`)
  supersedes it for structural claims, and both can drift from the actual `plugins/skoghooks/` code
  (see [plugins.md](plugins.md#skoghooks-drift-from-claudemd) for confirmed CLAUDE.md drift as a
  cautionary example — verify against the live tree before trusting any single doc).
- Two Node.js "ECC" subsystems exist in the repo (`plugins/skoghooks/scripts/{hooks,lib}/*.js` and
  `plugins/skogharness/scripts/`) that look related but weren't diffed — don't assume they're
  identical.
