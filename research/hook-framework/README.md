# Hook framework research

Research base for fixing the four earlier hook-framework attempts in this repo
against the architecture proven out by `claude-code-hooks` (a mature,
single-purpose sound-notification hook framework).

- [reference-architecture.md](./reference-architecture.md) — 16 architectural patterns worth reusing, plus the reference repo's install process.
- [attempts-review.md](./attempts-review.md) — per-attempt review of `.claude/hooks/`, `skogharness`, `skoghooks`, and `skogix-hooks` against those patterns.
- [plan.md](./plan.md) — cross-attempt gap list and fix priority order.

Next step: execute against `skogix-hooks` first (highest-priority gaps: real
drift between wired and on-disk scripts, no config file, no scaffold tooling).
