# Plan: Apply This Repo's Architecture to the 4 harness1 Hook-Framework Attempts

## Background

`/home/skogix/.local/src/harness1` contains four independent, earlier attempts at
building a Claude Code hook framework:

1. `.claude/hooks/` — raw, non-plugin (skill-activation/build-tracking framework)
2. `marketplace/plugins/skogharness/` — broadest scope (code-quality + telemetry, "ECC")
3. `marketplace/plugins/skoghooks/` — logging/context/validation hook set
4. `marketplace/plugins/skogix-hooks/` — multi-agent lesson-injection + quality-gate framework

None of the four purposes match this repo's (sound notification) — this plan is not
"port the sound hooks," it's "port the *architectural discipline* this repo has
proven out, into frameworks that do different things." Full findings live in:
- [reference-architecture.md](./reference-architecture.md) (16 patterns extracted from this repo)
- [attempts-review.md](./attempts-review.md) (per-attempt review, corrected)

## Scope

For each of the four attempts, close the gap against the patterns below, in priority
order. Skip patterns that don't fit an attempt's actual purpose (e.g. attempt 2's
blocking-by-design nature means "never block" doesn't apply the same way).

**Not in scope:** rewriting any attempt's actual feature logic (skill activation,
lesson matching, quality gates, etc.) — only the framework/plumbing layer around it.

---

## Cross-attempt gaps (present in 3 or all 4)

### Gap 1: No single dispatcher
All four use one-script-per-hook-event. The reference's `hooks.py` proves a single
dispatcher (read `hook_event_name` from stdin, dict-dispatch) scales to 30 events
without duplicating shared logic (fail-open wrapping, path guards, logging).

- **Where it matters most:** skoghooks (13 scripts) and skogix-hooks (17 scripts) —
  most duplicated boilerplate to collapse.
- **Where it's partially already true:** skogharness's `pre-bash-dispatcher.js`/
  `post-bash-dispatcher.js` and skogix-hooks' `stop.sh` (sub-dispatches to
  `stop-git-dirty.sh`/`stop-quality-gate.sh`) — finish the idea rather than reinvent it.
- **`.claude/hooks/`** — different tradeoff: several hooks are already logically
  distinct enforcement mechanisms (guard vs. tracker), so full collapse to one
  dispatcher may cost clarity. Lower priority here.

### Gap 2: No two-tier config (shared + personal-override)
None of the four have this repo's `hooks-config.json` + `hooks-config.local.json`
pattern with one shared `is_hook_disabled()` fallback function. Config today is env
vars (skogharness, `.claude/hooks/`), CLI flags baked into the manifest (skoghooks),
or path/env convention with no toggle at all (skogix-hooks).

- Add one JSON config file per framework with `disable<Event>Hook` keys, plus a
  gitignored `.local.json` override, plus one shared lookup function — not per-hook
  reimplementation.
- Independent axis: **logging/muting must be separate from disabling the hook's main
  effect** (`is_logging_disabled()` alongside `is_hook_disabled()`), per Pattern 8.

### Gap 3: No fail-open discipline centralized in one place
skoghooks has fail-open per-script (correct behavior, duplicated). skogix-hooks
asserts it only in prose (`AGENTS.md`), enforced ad hoc with `|| true`. skogharness
treats blocking as first-class by design (legitimate, not a gap there).

- Wherever a dispatcher gets introduced (Gap 1), put the `try/except -> sys.exit(0)`
  wrapper (or bash equivalent) in the dispatcher itself, once.

### Gap 4: No empirically-verified agent-hook subset
The reference tested which hooks actually fire in subagent sessions (6 of 30) rather
than trusting docs. None of the four attempts have done this for their own hook set.
Worth doing once, hooked into whichever dispatcher exists.

### Gap 5: No drift-detection discipline
This repo's `/workflows:workflow-changelog` + `verification-checklist.md` treats
"docs/config claiming something that isn't wired" as a bug class, checked on a
schedule. skogix-hooks currently has real drift (6/17 scripts wired); skoghooks does
**not** despite an earlier review pass wrongly claiming otherwise (see
attempts-review.md's skoghooks correction — its scaffold tooling at
`marketplace/scripts/` + `.claude/skills/new-hook/` is real and should be the model
here, not the target of this fix).

- Skogix-hooks needs an equivalent scaffold+drift-check pair before its 11 unwired
  scripts either get wired or deleted.

---

## Per-attempt priority

1. **skogix-hooks** — highest priority: real drift (11/17 unwired scripts), no config
   file, no scaffold/test tooling. User has already flagged this as next round's focus.
2. **skoghooks** — mostly sound; add two-tier config + collapse 13 scripts toward a
   dispatcher. Its scaffold+test trio is *already* the reference pattern — keep, don't
   replace.
3. **skogharness** — finish the partial dispatcher idea (bash dispatchers), add a
   config file to reduce the env-var sprawl; keep "hookify" and the profile system,
   both are genuine strengths not present in the reference.
4. **`.claude/hooks/`** — heaviest lift (npm/TS toolchain, env-var config sprawl) but
   also has real strengths (two-hook guard/tracker coordination, telemetry conversion
   stats) the reference never needed — treat as the lowest-priority, most-bespoke case.

## Verify

- [ ] Each framework has exactly one config file + one gitignored local-override file
- [ ] Each framework has one dispatcher (or one sub-dispatcher per sub-domain, documented as such)
- [ ] Fail-open wrapping lives in one place per framework, not per-script
- [ ] skogix-hooks' `hooks.json` wiring matches its scripts on disk (no dead scripts, no undocumented ones)
- [ ] Each framework's README hook-count/table matches its actual wired hooks (this repo's "consistency-as-correctness" discipline)

## Notes

- This plan intentionally stays at the architecture/pattern level per standing
  instruction: review and fix work should focus on the framework layer, not
  rewrite feature logic.
- Order of execution across the 4 attempts is not yet decided — this plan lists
  priority, not a commitment to do all four in one pass.
