# Directory Structure

*Last Updated: 2026-09-15*

## Repo root

```
marketplace/
├── .claude-plugin/marketplace.json   registers ONLY plugins/skoghooks (see plugins.md)
├── CLAUDE.md AGENTS.md README.md     document plugins/skoghooks; silent on the other 3 plugin dirs
├── scripts/
│   ├── new_hook.py                  scaffold a new skoghooks hook + wire it into hooks.json
│   └── test_hooks.py                smoke-test every wired skoghooks hook, expect exit 0
├── templates/hook_template.py        canonical hook skeleton new_hook.py scaffolds from
├── tests/payloads/                   14 JSON fixtures, one per lifecycle event (+1 extra scenario)
├── .todo/                            memory-agent scratch notes (mem:tech_stack, mem:conventions, ...)
└── plugins/
    ├── skoghooks/            (189 files) — REGISTERED plugin
    ├── skogharness/          (666 files) — vendored "ECC", own marketplace.json
    ├── skogix-hooks/         (1154 files) — "dot-core" incubator, Codex schema
    └── skogix-core-original/ (35 files) — routing Skill, no plugin manifest
```

## `plugins/skoghooks/`

```
plugins/skoghooks/
├── .claude-plugin/plugin.json
├── hooks/hooks.json              13 Python events + a spliced-in JS "ECC memory persistence" ref block
├── hooks/lesson_matcher.py, test_lesson_matcher.py, user-prompt-submit.sh   undocumented in CLAUDE.md
├── scripts/
│   ├── session_start.py .. pre_compact.py    13 hook entry points (documented in root CLAUDE.md)
│   ├── utils/            runtime_dir.py, jsonl_log.py, llm/{anth,oai,ollama,task_summarizer}.py,
│   │                      tts/{elevenlabs,openai,pyttsx3,tts_queue}.py
│   ├── validators/        ruff_validator.py, ty_validator.py, validate_file_contains.py, validate_new_file.py
│   ├── hooks/*.js         49 files — undocumented Node "ECC" hook dispatchers/trackers
│   └── lib/*.js           ~88 files — undocumented Node "ECC" libs (install-targets/, state-store/, ...)
└── tests/*.bats            skogai-jq.bats, user-prompt-submit.bats (separate from root scripts/test_hooks.py)
```

## `plugins/skogharness/`

```
plugins/skogharness/
├── .claude-plugin/plugin.json, marketplace.json   own marketplace, independent of repo root
├── AGENTS.md                 "Everything Claude Code (ECC)" overview — 67 agents/277 skills/92 commands
├── PLUGIN_SCHEMA_NOTES.md    undocumented plugin.json validator quirks (e.g. "agents" field forbidden)
├── agents/                   67 .md agent definitions
├── commands/                 92 .md slash-command definitions
├── skills/skogai/            ~80 skill folders (native Claude Code SKILL.md format)
├── .agents/skills/           37 skill folders (OpenAI agents/openai.yaml mirror format)
├── .agents/plugins/marketplace.json   third marketplace manifest, for the OpenAI-format mirror
├── rules/skogai/              per-language rule sets (angular, golang, python, rust, typescript, ...)
├── hooks/hooks.json           master lifecycle wiring, routed through run-with-flags.js bootstrap
├── hooks/memory-persistence/  separate sub-hook-system, own hooks.json + README
├── scripts/hooks/             48 Node hook implementation scripts
├── scripts/lib/                ~90 shared libs: install-targets/, session-adapters/, state-store/,
│                                skill-evolution/, control-pane/, github-coordination/, worktree-lifecycle/
├── ecc/install-state.json     install target/profile metadata
└── mcp-configs/mcp-servers.json   reference MCP server configs (nexus, jira/atlassian, ...)
```

## `plugins/skogix-hooks/` (`dot-core`)

```
plugins/skogix-hooks/
├── .codex-plugin/plugin.json   the ONLY manifest — no .claude-plugin/ dir at all
├── hooks.json                   wires 6 Codex-schema events to hooks/*.sh
├── AGENTS.md                    plugin-root map; every subdir has its own AGENTS.md router too
├── hooks/            (22 files) shell routers + lesson_matcher.py (Python)
├── skills/         (1093 files) skogai-jq (1083), skogai-gita (6), skogdocs, skogai-worktrunk,
│                                 skogai-hook-debugging
├── commands/         (12 files) legacy slash-command markdown shims
├── agents/            (2 files) code-reviewer.md, code-simplicity-reviewer.md
├── scripts/            (8 files) shared shell helpers (skogai-jq.sh, workflow-memory.sh, ...)
└── tests/             (11 files) Bats suites + test-helper.bash
```

`skills/skogai-jq/` breakdown: ~70 transform directories (e.g. `crud-get/`, `array-filter/`,
`extract-urls/`, `validate-*/`, `to-*/`, `is-*/`), each with `transform.jq`, `schema.json`, `test.sh`,
and 8-25 `test-input-N.json` fixtures. Also a `tasks/` dir (60 markdown backlog specs, planning docs
not runtime code).

## `plugins/skogix-core-original/` (`skogai-routing`)

```
plugins/skogix-core-original/
├── SKILL.md              canonical entry point (frontmatter: name: skogai-routing, type: router)
├── AGENTS.md CLAUDE.md SKOGAI.md   near-identical stub routers, all point back to SKILL.md
├── references/  (5 files)   at-linking.md, claude-md-routing-rules.md, naming-and-ownership.md, ...
├── workflows/   (9 files)   audit-framework.md, route-information.md, write-workflow.md, ...
├── templates/   (6 files)   agents-md.md, claude-md.md, reference-endpoint.md, ...
├── schemas/    (13 files)   README.md + 12 *.schema.json (decision, lesson, pattern, principle, ...)
└── scripts/     (4 files)   _validate_file.py, create-gh-issue.sh, list-xml-tags.sh, validate-schema.sh
```
