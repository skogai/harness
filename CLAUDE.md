# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Claude-specific notes

- `templates/` is a full self-referential copy of this repo's own scaffold (its own `src/`, `test/`, `AGENTS.md`, `.claude/`) used to bootstrap new harness installs. Edits under `templates/src/...` are template content, not this repo's runtime code — don't confuse the two trees.
- Package manager is `bun` (`bun@1.3.11` per `packageManager` in package.json). Prefer `bun install` / `bun test` / `bun run lint` over `npm`/direct `node` invocations where both work.
- This repo is actively being stripped down toward a "skogai agent runtime" (git log shows removal of Cursor support, legal/security docs, and most of an aspirational 40-skill marketplace — only `toon-formatter` and `harness-creator` skills remain live under `templates/.claude/skills/`). Don't assume README/marketplace copy describing "40 skills across 10 categories" (`.claude-plugin/README.md`) reflects current reality — it's stale/aspirational.

<harness:skills>
## Harness skills

Managed by `skogai.json` — run `npx --yes github:skogai/harness sync` after editing it, or `harness sync` if installed globally.

- `harness-creator`: Build, audit, and improve harnesses that make AI coding agents reliable: AGENTS.md/CLAUDE.md instruction files, feature/state tracking, verification gates, scope boundaries, session handoff, memory persistence, context budgets, tool-permission safety, and multi-agent coordination. Use this whenever a coding agent is unreliable across sessions — forgets context, drifts out of scope, claims "done" before tests pass, or starts each session inconsistently — or when creating or assessing AGENTS.md, CLAUDE.md, feature_list.json, init.sh, progress.md, or session-handoff files. Reach for it even if the user never says the word harness.
- `toon-formatter`: Guidance on when and how to use TOON (Token-Oriented Object Notation) — a compact JSON alternative that typically cuts input tokens 30-50% on tabular data. Use when the user is about to paste or serialize a large JSON array into a prompt, has a payload with ≥5 uniform objects, or is optimizing an LLM pipeline for cost/context. Knows the format shapes (tabular `[N]{a,b}:` rows, inline `[N]: ...`, expanded), when TOON helps vs hurts, and how to invoke installed TOON commands or wrappers when available. Example queries — "convert this API response to TOON", "will this JSON benefit from TOON", "how does TOON handle nested objects".
- `agent-entrypoint-design`: Use when designing or refactoring AGENTS.md, CLAUDE.md, GEMINI.md, Cursor rules, GitHub instructions, source-of-truth navigation, or agent onboarding entrypoints.
- `agent-ledger-and-delivery`: Use when designing agent_chats or agents_chat records, delivery evidence summaries, linked tasks or commits, validation notes, risks, review notes, or handoff records.
- `atomic-commit-discipline`: Use when splitting changes into atomic commits, preparing commits from mixed worktrees, staging exact paths, including related task-state updates, writing Conventional Commits, or preventing unrelated changes.
- `design-doc-and-task-board`: Use when deciding how requirements should be captured in design docs, tasks.md, external task systems, exec plans, acceptance criteria, status updates, or planning source-of-truth files.
- `quality-gardening`: Use when designing quality snapshots, generated quality reports, structural metrics, debt thresholds, regression budgets, quality gates, or gradual cleanup loops.
- `repo-contracts-and-boundaries`: Use when turning architecture, layering, directory ownership, dependency direction, file-size limits, choke points, baselines, or allowlists into repository checks.
- `repo-harness-assessment`: Use when evaluating an existing repository's agent-readiness, harness maturity, validation surfaces, source-of-truth docs, evidence artifacts, or next smallest harness improvement.
- `runtime-evidence-and-tracing`: Use when connecting observed behavior, logs, metrics, request IDs, run IDs, screenshots, traces, external dependency results, or artifacts into a runtime evidence loop.
- `validation-harness-design`: Use when designing repository validation commands, doctor scripts, test matrices, JSON or JUnit outputs, CI gates, smoke checks, or harness command surfaces.
</harness:skills>
