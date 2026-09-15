# Key Modules

*Last Updated: 2026-09-15*

The largest/most central files per plugin — not exhaustive, see [directory-structure.md](directory-structure.md)
for full trees.

## `plugins/skoghooks/`

- `scripts/utils/runtime_dir.py` — resolves the session-scoped tmp runtime dir every hook logs to.
- `scripts/utils/jsonl_log.py` — `append_jsonl()`, the shared logging primitive every hook script calls.
- `scripts/utils/llm/{anth,oai,ollama,task_summarizer}.py` — LLM client wrappers (priority order for
  completion-message generation per root CLAUDE.md: openai > anthropic > ollama > random, referenced
  by `stop.py`).
- `scripts/utils/tts/{elevenlabs_tts,openai_tts,pyttsx3_tts,tts_queue}.py` — TTS backends (root
  CLAUDE.md states "No TTS" for the distributed config, but the code exists and is wired for local use).
- `scripts/validators/{ruff_validator,ty_validator,validate_file_contains,validate_new_file}.py` —
  used by the `/new-hook` skill workflow to validate scaffolded hooks.
- `hooks/lesson_matcher.py` — undocumented in CLAUDE.md; likely shared code with
  `plugins/skogix-hooks/hooks/lesson_matcher.py` (same filename, same purpose — not diffed).
- Undocumented JS subsystem: `scripts/hooks/*.js` (49) + `scripts/lib/*.js` (~88) — not individually
  cataloged; see [plugins.md](plugins.md#skoghooks-drift-from-claudemd) for what's known.

## `plugins/skogharness/`

- `skills/skogai/continuous-learning-v2/scripts/instinct-cli.py` (1956 lines) — CLI for a "continuous
  learning / instinct" system; the largest file in the entire repo, and the only module with a real
  test suite (`test_parse_instinct.py`, 1421 lines).
- `scripts/hooks/gateguard-fact-force.js` (1238 lines) — "Fact-forcing gate": blocks the first
  Edit/Write/MultiEdit per file and demands investigation first (a PreToolUse guard).
- `scripts/lib/install-lifecycle.js` (1160) + `install-executor.js` (782) + `install-manifests.js`
  (708) — the installer subsystem pushing ECC/skogharness config into other tools' home/project dirs
  (`scripts/lib/install-targets/*.js`: claude-home, cursor-project, codex-home, gemini-project,
  zed-project, and more).
- `scripts/harness-audit.js` (1082 lines) — backs the `/harness-audit` slash command.
- `scripts/lib/state-store/queries.js` (906) + `schema.js` + `migrations.js` — embedded state-store
  for session/metrics persistence.
- `scripts/hooks/mcp-health-check.js` (749) — MCP health polling and reconnect on PostToolUseFailure.
- `scripts/hooks/session-activity-tracker.js` (639) — per-session tool/file activity tracking.
- `scripts/hooks/session-start.js` (723) — real SessionStart logic; invoked via a thin
  `session-start-bootstrap.js` wrapper that exists solely to dodge a shell `!`-history-expansion bug
  from an earlier `node -e "..."` inline-hooks.json approach.
- `scripts/lib/control-pane/` — self-contained mini dashboard/server (`server.js`, `ui.js` 696 lines,
  `state.js` 675 lines) for observing agents, with a proximity visualization.
- `scripts/setup-package-manager.js` — detects the *host* project's package manager; this plugin has
  no deps of its own to install.

## `plugins/skogix-hooks/` (`dot-core`)

- `hooks/pre-tool-use.sh` (145 lines) — the guardrail: regex-blocks `rm -rf /`, force-push to
  main/master, `chmod 777`, `curl|sh`, `dd of=/dev/*`, `mkfs`, `.env` reads/exfiltration; exits 2 to
  block. Contrast with `plugins/skoghooks/scripts/pre_tool_use.py`, whose equivalent blocking logic
  (`is_dangerous_rm_command()`, `is_env_file_access()`) is present but **disabled** — this plugin's
  guardrail is live.
- `hooks/lesson_matcher.py` (377 lines) + `test_lesson_matcher.py` (661 lines) — reads gptme-format
  lessons (YAML frontmatter + markdown) from `$HOME/.skogai/knowledge/lessons`, matches by mode
  (session-start/prompt/tool), caps results (session 3, prompt 3, tool 2), skips
  README/TEMPLATE/dated notes and `status: deprecated|archived`.
- `scripts/skogai-jq.sh` (75 lines) — shared JSON field/log/response helpers used across hooks.
- `skills/skogai-jq/*/transform.jq` — ~70 small (5-40 line), dependency-free jq transforms, each
  schema-first and independently tested.

## `plugins/skogix-core-original/` (`skogai-routing`)

- `SKILL.md` — the router entry point; everything else in the directory exists to be referenced from
  or written according to it.
- `schemas/*.schema.json` (12 files) — JSON Schemas for decision, defs, document, frontmatter, lesson,
  list, pattern, principle, reference, router, script, skill, template — the structural contracts the
  routing framework enforces.
- `scripts/_validate_file.py` — validates a file against its declared schema.
