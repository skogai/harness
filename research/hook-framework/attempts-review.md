# Hook framework attempts — review

Comparing the four earlier hook-framework attempts living in this repo against the
reference implementation at `/home/skogix/.local/src/claude-code-hooks` (a mature,
single-purpose sound-notification hook system). Goal: extract what's good/bad in each
attempt so we know what to keep, fix, or drop.

Reference repo's good parts are written up separately at:
[reference-architecture.md](./reference-architecture.md)

The four attempts, all inside this repo:
1. `.claude/hooks/` — raw, non-plugin version
2. `marketplace/plugins/skogharness/hooks/`
3. `marketplace/plugins/skoghooks/hooks/`
4. `marketplace/plugins/skogix-hooks/hooks/`

(`.codex/hooks` also exists but is Codex-CLI-side, not a Claude Code hook framework attempt.)

---

## 1. `.claude/hooks/` (raw, non-plugin)

**Purpose:** different from the reference repo — not sound notifications, but skill
auto-activation enforcement, file/build tracking, and session intelligence.

**Essential hooks:**
- `skill-activation-prompt` (UserPromptSubmit) — reads `skill-rules.json`, matches prompt/file context, injects skill suggestions.
- `post-tool-use-tracker` (PostToolUse) — tracks edited files, auto-detects project structure (frontend/backend/db/monorepo), caches for context.
- `skill-verification-guard` (PreToolUse) — enforces mandatory skills before Edit/Write/MultiEdit: blocks the *first* attempt with a reminder, allows the *second* (two-try model).
- `skill-activation-tracker` (PostToolUse: Skill matcher) — clears the pending-skill list once a skill actually activates, so the guard stops blocking.

**Optional/heavier hooks:** `tsc-check` (Stop, needs manual service-list editing), `trigger-build-resolver` (Stop, launches an auto-error-resolver agent on build failure), `stop-build-check-enhanced`, `error-handling-reminder`, `session-doc-updater` (indexes active dev-docs into a local vector DB, no-ops until configured).

**Architecture notes:**
- One script per hook event (often a paired `.sh` + `.ts`), not a single dispatcher.
- Requires `npm install` + a TypeScript toolchain — real dependency footprint vs. reference's stdlib-only Python.
- Config is spread across many env vars (`SKIP_MANDATORY_SKILLS`, `PRETOOLUSE_SOFT_BLOCK`, `SKILL_AI_PROVIDER`, etc.) rather than one two-tier JSON config file.
- Customization for several hooks means editing shell `case` statements *inside* the hook scripts (service names, build commands, tsconfig paths) — brittle, per-project surgery rather than config-driven.
- Has an AI-provider abstraction (gemini/openai/anthropic/ollama) for skill classification, suggest-only by default (won't arm hard blocks without explicit opt-in) — justified by a stated false-positive rate from real benchmarking. Heavy, but the guardrail-by-default design is sound.
- Telemetry: one JSONL line per suggest/activate/block event, rotates at 10MB, excludes benchmark sessions from real-usage stats. Has its own `skill-stats.sh` report (suggest→activate conversion per skill, block counts by kind) — a real feedback loop, not just a log.
- Has a Codex-CLI compatibility adapter (`.codex/hooks.json` + `_codex-adapter.sh`) reusing the same scripts across two CLI tools without forking code.

**My take:**
- *Diverges from reference's good parts on:* no single dispatcher (more files to touch for shared-logic changes), heavier deps, config sprawled across env vars instead of a clean local-override JSON file, brittle in-script customization.
- *Ahead of the reference on:* a genuine two-hook enforcement/coordination pattern (guard + tracker) — the reference never needed this since sound hooks never block. Also ahead on telemetry depth (conversion stats, not just an audit log) and on cross-tool (Codex) reuse.

---

## 2. `marketplace/plugins/skogharness/` (aka "ECC" — everything-claude-code)

**Purpose:** the broadest of the four — code-quality/safety enforcement (dangerous-Bash blocking, config-file protection, GateGuard fact-forcing before edits), automated checks (format/typecheck/lint at Stop, console.log and doc-file warnings), plus a whole "continuous learning" telemetry subsystem (tool-use logging, session metrics, cost tracking, pattern extraction). A superset of concerns, not a single-purpose framework.

**Architecture notes:**
- ~30+ hook entries across 7 event types (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SessionStart`, `SessionEnd`, `PreCompact`), defined in `hooks/hooks.json`.
- NOT a single dispatcher — one Node.js script per behavior in `scripts/hooks/*.js` (~30 files). Two "consolidated dispatcher" scripts (`pre-bash-dispatcher.js`, `post-bash-dispatcher.js`) combine several Bash-matcher checks, but that's the exception, not the rule.
- Runtime is Node.js, invoked via an inline `node -e "..."` bootstrap that re-implements plugin-root discovery, copy-pasted verbatim into ~20 `hooks.json` command strings — the opposite of "one fallback function, reused."
- Three different runtimes coexist: Node (`scripts/hooks/*.js`), bash+Python (`continuous-learning-v2/hooks/observe.sh`), and a markdown rule-DSL layer ("hookify": `.claude/hookify.*.local.md` with YAML frontmatter + regex conditions).
- Config is env-var only: `ECC_HOOK_PROFILE=minimal|standard|strict`, `ECC_DISABLED_HOOKS=<comma-list>`, plus a dozen single-purpose toggles, centralized in one `hook-flags.js` helper. No two-tier file-based local override.

**Divergences from reference's good parts (weaknesses):**
- No single dispatcher, no two-tier config file, heavy copy-pasted boilerplate instead of a shared helper.
- Blocking is a first-class feature here (GateGuard, dangerous-Bash guard, dev-server-outside-tmux blocker) — so "never break the session" isn't a universal design axiom; that's a legitimate scope difference, not a bug, but it does mean no fail-open guarantee at the framework level.
- No hook-count consistency discipline or automated drift-detection workflow equivalent.

**Strengths worth keeping:**
- A **profile system** (`minimal/standard/strict`) — one global dial across all hooks, more ergonomic than toggling each individually (trades off per-hook local-override granularity, though).
- The Bash dispatchers show partial movement toward "one dispatcher," just not applied plugin-wide — worth finishing that idea rather than reinventing it.
- **"Hookify"**: an end-user-authorable rule engine (markdown+YAML+regex, no code) for defining new hook-like behavior — something the reference's code-only `BASH_PATTERNS` table can't do.
- `PLUGIN_SCHEMA_NOTES.md` documents hard-won plugin-manifest validator quirks with a flip-flop history table and commit hashes — the same "treat gotchas as a regression surface" instinct as the reference's `HOOKS-README.md`, just applied to the manifest schema instead of the hook count.
- The `observe.sh` telemetry pipeline has real defensive engineering: flock-based counter locking with mkdir fallback, a SIGALRM self-timeout ahead of the hook's own timeout to avoid orphaned processes, secret-scrubbing before persisting tool I/O, and explicit exclusion of non-human/self-referential sessions — more careful than the reference's fail-open model needed to be, appropriate for a much riskier (data-capturing) hook.

---

*(Attempt 3 to be added below as reviewed.)*

## 4. `marketplace/plugins/skogix-hooks/`

**Purpose:** a multi-agent workflow-support harness — injects "lessons" and prior context at session/prompt/tool boundaries, enforces quality gates (git-dirty warnings, lint/test checks) at Stop, and hooks git-worktree lifecycle events. Closer to a context-injection + guardrail framework than a notifier, and aware of Codex as well as Claude Code.

**Architecture notes:**
- ~17 shell scripts in `hooks/`, one per hook event, not a single dispatcher (`session-start.sh`, `user-prompt-submit.sh`, `pre-tool-use.sh`, `post-tool-use.sh`, `stop.sh`, `worktree-create.sh`, `teammate-idle.sh`, etc.).
- Runtime: bash + a shared library `scripts/skogai-jq.sh` (sourced by every script — stdin JSON parsing, session/event extraction, JSONL debug logging, `skogai_jq_context`/`skogai_jq_decision` helpers), plus one Python component: `hooks/lesson_matcher.py` (YAML-frontmatter lesson search/scoring with a stdlib fallback if PyYAML is missing), with its own test file.
- `stop.sh` is a mini sub-dispatcher, calling out to `stop-git-dirty.sh` and `stop-quality-gate.sh` — a "sub-dispatcher per event" pattern, distinct from the reference's flat single dispatcher.
- Registered via `hooks.json` (Claude Code) and mirrored in `.codex-plugin/plugin.json`/`.app.json` for Codex.
- Config is path/env convention (default lesson dirs under `~/.skogai/knowledge/lessons`, `~/.config/skogai/lessons`, etc.), not a settings file with toggles — no local-override config file, no `disableAllHooks`/mute mechanism.

**Divergences from reference's good parts (weaknesses):**
- No single dispatcher, so no central place to enforce hook-count consistency.
- **Real drift found**: `hooks.json` only wires 6 of the ~17 scripts that exist on disk (SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PermissionRequest, Stop) — 11 scripts (`config-change.sh`, `notification.sh`, `pre-compact.sh`, `session-end.sh`, `subagent-start.sh`, `subagent-stop.sh`, `task-completed.sh`, `teammate-idle.sh`, `worktree-create.sh`, `worktree-remove.sh`, `post-tool-use-failure.sh`) are dead code — exactly the failure mode the reference's "consistency-as-correctness" discipline exists to prevent.
- No two-tier config, no independent logging/mute toggle (`skogai_jq_log` always writes to `/tmp/${session_id}.jsonl` with no visible disable).
- Fail-open is asserted only in prose (`hooks/AGENTS.md`: "Context injection is fail-open... must not block the user turn") rather than enforced by one shared function — each script individually has to `|| true` its risky calls.
- No path-traversal guard evident in `lesson_matcher.py`'s directory scanning.
- No empirically-verified agent-hook-behavior map or hook-addition/drift-detection workflow.

**Strengths worth keeping:**
- `lesson_matcher.py` is a genuinely more sophisticated content-matching engine than the reference needs — YAML-frontmatter parsing with stdlib fallback, keyword/score-based matching, `always_apply` flag, skip-list for README/TEMPLATE/archived-status files. Worth mining as a generalization of the reference's "extensible pattern table" idea, applied to structured knowledge injection instead of sound-name lookup.
- `scripts/skogai-jq.sh` is a reasonable shared-library analog to the reference's reusable helper functions, just for JSON I/O instead of config state.
- Broader hook *coverage in scripts* (worktree create/remove, task-completed, teammate-idle) shows real multi-agent/orchestration awareness the single-user reference never needed — even though most of it isn't wired up yet.
- **Uncommitted change** to `lesson_matcher.py` right now is a reformat + rebrand ("gptme format" → "skogai format") plus an expanded lesson-search path list pulling in conventions from other agent tools (Goose, Amy, gptme lineage) — signals a cross-agent lesson-sharing direction, not a dispatch-architecture change.

---

## 3. `marketplace/plugins/skoghooks/`

**Purpose:** a logging/context/validation hook set — wires a handler into every lifecycle event (session start/end, prompt submit, tool use/failure, permission request, notification, stop, subagent start/stop, pre-compact, setup) to log activity, load git/context info at session start, block dangerous commands (`rm -rf`, `.env` reads), and optionally summarize transcripts. Not a sound-notification system.

**Architecture notes:**
- 13 separate Python scripts, one per hook event (`session_start.py`, `pre_tool_use.py`, `stop.py`, etc.) — one-per-hook, the inverse of the reference's single `hooks.py` dispatcher.
- Runtime: `uv run --script` (PEP 723 inline-deps Python 3.11+) — each script is self-contained with its own declared deps, no shared `requirements.txt`.
- Wiring lives in `hooks/hooks.json`; behavior is controlled entirely via CLI flags baked into that file per event (`--log-only`, `--chat`, `--backup`, `--load-context`) plus a couple of env vars — no config file, no two-tier local-override mechanism.
- Fail-open is present and confirmed in the active scripts (try/except around JSON parsing and general exceptions, both falling through to `sys.exit(0)`) — matches the reference's core safety property, just not centralized in one function.

**Divergences from reference's good parts (weaknesses):**
- No dispatcher — 13 files instead of one, so any shared logic (fail-open wrapper, path guards) is duplicated per-script rather than centralized.
- No config file / no two-tier override — changing behavior means editing the committed `hooks.json` manifest directly, not a personal override file.
- No independent logging/muting toggle analogous to `is_hook_disabled`/`is_logging_disabled`.
- No empirically-verified agent-hook subset mapping.
- A large, unrelated second hook system (~150 files under `scripts/hooks/*.js` — install targets for six other AI tools, a control-pane server, cost-tracker, tmux-worktree-orchestrator, etc.) sits in the same tree, wired only through a separate `memory-persistence/hooks.json` that itself labels it "reference... production hook graph is `hooks/hooks.json`." Vestigial, but muddies which hooks are actually real.
- A path-traversal guard (`scripts/lib/path-safety.js`) exists, but only in that unused JS tree — not shared with the active Python hooks that would benefit from it.

**Correction (previous pass got this wrong):** an earlier review claimed the README's scaffold tooling (`new_hook.py`, `hook_template.py`, `test_hooks.py`, a `new-hook` skill) "doesn't exist," because the search only looked inside `marketplace/plugins/skoghooks/`. It's real — it just lives one level up, at the `marketplace/` root, plus a skill at the repo root:
- `marketplace/scripts/new_hook.py` (108 lines) — scaffolds `plugins/skoghooks/scripts/<name>.py` from `marketplace/templates/hook_template.py`, appends the command to `plugins/skoghooks/hooks/hooks.json`.
- `marketplace/templates/hook_template.py` (56 lines) — the hook contract as boilerplate: stdin JSON in, `try/except: pass` wrapping, exit 0 always, `sys.exit(2)` only to deliberately block, logging via `append_jsonl(get_runtime_dir(session_id) / "{name}.jsonl")`, a `hookSpecificOutput`/`additionalContext` comment stub.
- `marketplace/scripts/test_hooks.py` (83 lines) — reads `plugins/skoghooks/hooks/hooks.json`, pipes each wired event's fixture from `tests/payloads/<Event>.json` through the exact command string (with `CLAUDE_PLUGIN_ROOT` resolved), asserts exit 0, reports PASS/FAIL per hook. Its `PLUGIN_ROOT` constant is hardcoded to `plugins/skoghooks` — so despite sitting at the shared marketplace root, this specific tool is skoghooks-only, not a generic multi-plugin scaffolder.
- `.claude/skills/new-hook/SKILL.md` (repo root, 80 lines) — a genuine 6-step workflow (Scaffold → Implement → Test → Validate the plugin → Document → Commit) that wraps the three scripts above into one skill, explicitly modeled on getting a new hook fully wired and tested, not just stubbed. This is a real, functional analog to the reference repo's `/workflows:workflow-add-hook`, just scoped to one plugin and living outside any plugin directory.
- **Test coverage was also under-reported.** `plugins/skoghooks/tests/skogai-jq/skogai-jq.bats` is a real 286-line, 26-test bats suite covering the shared `skogai-jq.sh` library end to end: stdin-JSON capture, session_id/event extraction (with defaults), `skogai_jq_field` (nested paths, missing-field defaults, null handling), `skogai_jq_log` (JSONL append, full-input embed), `skogai_jq_context` (valid JSON, `hookSpecificOutput` shape, special-char escaping), and `skogai_jq_decision` (decision/reason fields, `continue`). The identical file (byte-for-byte, confirmed via `diff`) also exists under `plugins/skogix-hooks/tests/skogai-jq/skogai-jq.bats` — the two plugins share both the library and its test suite.

**Strengths worth keeping:**
- Per-session runtime-dir scoping (`scripts/utils/runtime_dir.py` derives `<tmp_base>/skoghooks/<session_id>/` from the session's own JSON payload) — cleanly avoids concurrent-session log clobbering, arguably cleaner than the reference's single shared log file.
- README has an unusually honest "Non-Obvious Behaviours" table and an "active flags vs. other supported flags" table per script, explicitly noting what's wired vs. unwired (TTS, `--announce`, `--auto-allow`).
- `pre_tool_use.py` has real security-relevant blocking logic (regex-based `rm -rf` and `.env`-access blocking via `sys.exit(2)`) — something the sound-only reference doesn't attempt at all.
- A separate `validators/` directory (`ruff_validator.py`, `ty_validator.py`, `validate_new_file.py`, `validate_file_contains.py`) keeps validation logic composable and apart from the event scripts themselves.
- **The scaffold+test+skill trio above is the closest thing among all four attempts to the reference's `/workflows:workflow-add-hook` + bats-verified shared library** — real scaffolding, a real smoke-test runner keyed off the actual `hooks.json`, and a real, passing unit-test suite for the shared bash helpers. Worth carrying forward largely as-is into a rebuild, just relocated so the scaffold tooling lives inside (or clearly next to) the plugin it targets instead of one directory above it.

---

## Cross-attempt summary

All three plugin attempts (2–4) independently arrived at **one-script-per-hook-event** instead of the reference's single dispatcher, and none has a two-tier (shared + personal-override) config file — config is env vars, CLI flags baked into the manifest, or nothing. Every attempt that logs also lacks an independent mute-vs-log toggle. skogix-hooks has real drift: `hooks.json` only wires 6 of ~17 scripts on disk. skoghooks does *not* have the drift an earlier pass claimed — its scaffold tooling (`new_hook.py`/`hook_template.py`/`test_hooks.py`) and its `skogai-jq.bats` test suite are both real and functional, just located at the `marketplace/` root and repo-root `.claude/skills/new-hook/`, one level above the plugin dir the earlier pass searched. **Lesson for future review passes:** search the repo/marketplace root for shared tooling before concluding something documented in a plugin's README doesn't exist — plugin-scoped searches will produce false negatives on shared scaffolding.

Genuine strengths worth carrying into a rebuild: skogharness's end-user-authorable "hookify" rule engine and profile system, skogix-hooks' `lesson_matcher.py` content-matching engine, skoghooks' per-session runtime-dir scoping, and skoghooks' scaffold+test+skill trio (`new_hook.py` + `test_hooks.py` + `.claude/skills/new-hook`) as the closest existing analog to the reference's `/workflows:workflow-add-hook`.

**Next round:** deeper pass on `marketplace/plugins/skogix-hooks/` — the 11 unwired scripts, `lesson_matcher.py` in full, and its own `skogai-jq.bats` copy (shared with skoghooks, already covered above).
