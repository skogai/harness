# Entry Points

*Last Updated: 2026-09-15*

Execution in this repo starts at Claude Code (or Codex) lifecycle hook invocations, not a
traditional `main()`. Each plugin wires its own `hooks.json`.

## `plugins/skoghooks/` — `hooks/hooks.json` (13 Claude Code events)

| Event | Script | Active flags |
|---|---|---|
| SessionStart | `scripts/session_start.py` | `--load-context` |
| SessionEnd | `scripts/session_end.py` | — |
| Setup | `scripts/setup.py` | — |
| PreToolUse | `scripts/pre_tool_use.py` | — |
| PostToolUse | `scripts/post_tool_use.py` | — |
| PostToolUseFailure | `scripts/post_tool_use_failure.py` | — |
| UserPromptSubmit | `scripts/user_prompt_submit.py` **and** `hooks/user-prompt-submit.sh` (undocumented second command) | `--log-only` |
| PermissionRequest | `scripts/permission_request.py` | `--log-only` |
| Notification | `scripts/notification.py` | — |
| Stop | `scripts/stop.py` | `--chat` |
| SubagentStart | `scripts/subagent_start.py` | — |
| SubagentStop | `scripts/subagent_stop.py` | `--chat` |
| PreCompact | `scripts/pre_compact.py` | `--backup` |

Full flag reference and non-obvious behaviors are in root `CLAUDE.md` — accurate for the 13 Python
scripts; see [plugins.md](plugins.md#skoghooks-drift-from-claudemd) for what it misses.

`hooks/hooks.json` also carries a spliced-in reference block (separate `"events"` array pointing at
the undocumented `scripts/hooks/*.js` files, labeled "ECC memory persistence") that duplicates
`hooks/memory-persistence/hooks.json` — treat as dead/reference wiring, not confirmed live.

## `plugins/skogharness/` — `hooks/hooks.json` (every command routed through a bootstrap wrapper)

Every command is `plugin-hook-bootstrap.js` → `scripts/hooks/run-with-flags.js` (resolves
`CLAUDE_PLUGIN_ROOT` with fallbacks scanning `~/.claude/plugins/cache/{ecc,everything-claude-code}/...`
— built to survive being installed under either the "ecc" or "skogharness" name) before delegating to
the real handler.

| Event | Matcher | Scripts |
|---|---|---|
| PreToolUse | Bash | `pre-bash-dispatcher.js` (quality/tmux/push/GateGuard preflight) |
| PreToolUse | Write | `doc-file-warning.js` |
| PreToolUse | Edit\|Write | `suggest-compact.js` |
| PreToolUse | * | `observe-runner.js`, `mcp-health-check.js` |
| PreToolUse | Bash\|Write\|Edit\|MultiEdit | `governance-capture.js` |
| PreToolUse | Write\|Edit\|MultiEdit | `config-protection.js` (blocks edits to linter/formatter configs), `gateguard-fact-force.js` (blocks first Edit/Write per file, demands investigation first) |
| PostToolUse | Bash | `post-bash-dispatcher.js` |
| PostToolUse | Edit\|Write\|MultiEdit | `quality-gate.js`, `design-quality-check.js`, `post-edit-accumulator.js` |
| PostToolUse | Edit | `post-edit-console-warn.js` |
| PostToolUse | Bash\|Write\|Edit\|MultiEdit | `governance-capture.js` |
| PostToolUse | * | `session-activity-tracker.js`, `observe-runner.js`, `ecc-metrics-bridge.js`, `ecc-context-monitor.js` |
| PostToolUseFailure | * | MCP failure tracking/reconnect (in `mcp-health-check.js`) |
| PreCompact | * | `pre-compact.js` (save state before compaction) |
| SessionStart | * | `session-start-bootstrap.js` → `session-start.js` (loads prior context, detects package manager) |
| Stop | * | `stop-format-typecheck.js` (batch Biome/Prettier + tsc), `check-console-log.js`, `session-end.js`, `evaluate-session.js`, `cost-tracker.js`, `desktop-notify.js` |
| SessionEnd | * | `session-end-marker.js` (non-blocking) |

A second, independent sub-hook-system lives at `hooks/memory-persistence/hooks.json` with its own
README — not covered above.

## `plugins/skogix-hooks/` — `hooks.json` (6 Codex-schema events)

| Event | Script |
|---|---|
| SessionStart | `hooks/session-start.sh` (sources `scripts/workflow-memory.sh`, calls `scripts/session-context.sh`, invokes `lesson_matcher.py`) |
| UserPromptSubmit | `hooks/user-prompt-submit.sh` |
| PreToolUse | `hooks/pre-tool-use.sh` (guardrail — blocks `rm -rf /`, force-push to main/master, `chmod 777`, `curl\|sh`, `dd of=/dev/*`, `mkfs`, `.env` read/exfil patterns; exit 2 to block) |
| PermissionRequest | `hooks/permission-request.sh` (logs only) |
| PostToolUse | `hooks/post-tool-use.sh` (logs only, 25 lines) |
| Stop | `hooks/stop.sh` (fans out internally to `stop-git-dirty.sh` / `stop-quality-gate.sh`) |

11 more hook scripts exist **unwired** in `hooks/` (`post-tool-use-failure.sh`, `pre-compact.sh`,
`session-end.sh`, `subagent-start.sh`, `subagent-stop.sh`, `task-completed.sh`, `teammate-idle.sh`,
`worktree-create.sh`, `worktree-remove.sh`, `config-change.sh`, `notification.sh`) — the Codex hook
schema this plugin targets only supports the 6 events above.

Also: `commands/*.md` (12 legacy slash-command shims) and `skills/*/SKILL.md` (skill routing entry
points, frontmatter `name`/`description`/`permalink`).

## `plugins/skogix-core-original/` — no lifecycle wiring

Entry point is `SKILL.md` (skill invocation, not a hook event). No `hooks.json` anywhere in this
directory.

## Root scaffolding entry points (not lifecycle hooks)

- `scripts/new_hook.py <Event> <name> [--matcher ...] [--flags=...]` — scaffolds a new
  `plugins/skoghooks` hook from `templates/hook_template.py` and wires it into
  `plugins/skoghooks/hooks/hooks.json`.
- `scripts/test_hooks.py` — pipes each `tests/payloads/<Event>.json` fixture through the exact
  commands wired in `plugins/skoghooks/hooks/hooks.json`, expects exit 0 from every one.
