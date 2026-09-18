# Hook plugin engine audit

Date: 2026-09-16

## Scope

This audit treats the existing hook behaviors as disposable. It examines the
machinery around them: plugin loading, event registration, command dispatch,
configuration, logging, add/change/remove workflows, fixtures, tests,
validation, and drift control.

The three live plugin attempts are:

- `marketplace/plugins/skogharness`
- `marketplace/plugins/skoghooks`
- `marketplace/plugins/skogix-hooks`

The former repository-local `.claude/hooks` attempt was removed in commit
`5e5f413`, so older documents that describe four live attempts are stale.

## Executive finding

None of the three plugins currently provides one stable hook engine.

`skogharness` has a partial dispatcher buried behind a large runtime and
duplicated command bootstraps. `skoghooks` launches a separate program for
each event. `skogix-hooks` shares a shell library, but active hooks frequently
bypass it and its registry covers only a subset of the scripts on disk.

The reusable foundation is much smaller than any plugin:

1. Host-native plugin loading and event registration.
2. One representative payload fixture per event.
3. Executing the exact registered command in tests.
4. A small append-only JSONL writer.
5. One consistency check joining the registry, supported events, commands,
   and fixtures.

Everything else should have to earn its way back after that contract works.

## Current systems

### `skogharness`: broad framework and parts bin

- Claude loads `hooks/hooks.json` by convention. The plugin deliberately does
  not declare that conventional path in its manifest because newer Claude
  versions reject duplicate registration. This hard-won rule is documented in
  `PLUGIN_SCHEMA_NOTES.md`.
- The 354-line registry contains 27 hook groups across seven events. Most
  commands repeat inline Node root-discovery and spawn wrappers
  (`hooks/hooks.json`).
- The execution chain is typically registry bootstrap ->
  `plugin-hook-bootstrap.js` -> `run-with-flags.js` -> behavior module.
- `bash-hook-dispatcher.js` is the closest thing to a central dispatcher, but
  it handles only a subset of Bash-related behavior.
- Configuration is split across environment variables, JSON command
  arguments, and dispatcher-owned arrays. There is no authoritative registry.
- Installation documentation refers to absent installer scripts and manifest
  inputs. Version and source metadata also disagree between marketplaces.
- Claims of regression tests refer to test files absent from this snapshot.
  There is no plugin-local CI.

Useful ideas: conventional loading, bounded stdin, path confinement, and a
single dispatcher. Do not reuse the installer, behavior profiles, duplicated
bootstraps, or session machinery for the recorder MVP.

### `skoghooks`: closest recorder-shaped attempt

- The marketplace correctly points to this Claude plugin, whose conventional
  `hooks/hooks.json` is host-loaded.
- The registry names 13 lifecycle events but launches 14 commands because
  `UserPromptSubmit` has two handlers (`hooks/hooks.json`).
- The same registry contains `description` and `events` metadata inside its
  `hooks` object. Live `claude plugin validate` reports both as unknown events
  and ignores them at runtime.
- The smoke runner iterates every registry key but treats missing fixtures as
  skips. It therefore hides those invalid keys instead of failing
  (`marketplace/scripts/test_hooks.py`).
- Twelve commands use `uv`; several scripts declare `python-dotenv` even though
  they call it optional. In a clean/offline run this caused seven of fourteen
  command invocations to fail while trying to contact PyPI.
- The actual shared core is only `runtime_dir.py` plus `jsonl_log.py`. The
  latter writes both a session/event file and an undocumented global mirror at
  `~/.claude/data/skoghooks.jsonl`.
- Record shapes vary by event: raw payload, mutated payload, and envelopes are
  all used. There is no schema or schema version.
- `session_id` is used as a path component without validation. Logging has no
  concurrency, atomicity, retention, redaction, or strict output assertion.
- `new_hook.py` scaffolds another process and duplicates the supported-event
  list. There is no update or remove workflow.
- The runner's strong idea is executing exact registry commands with real
  fixtures and a timeout. Its weak assertion is exit code only; broad
  fail-open handlers can pass without writing anything.
- There is no test CI. The repository's only GitHub workflow responds to
  `@claude` mentions.

Compression evidence: this plugin has 189 tracked files; 144 are in copied
`scripts/hooks` and `scripts/lib` subtrees unrelated to the active Python
lifecycle registry.

Useful ideas: marketplace packaging, `${CLAUDE_PLUGIN_ROOT}`, fixture-per-event,
exact-command smoke execution, and a test-configurable runtime directory.

### `skogix-hooks`: tested behavior around an untested engine

- This is not registered in the Claude marketplace. Its only plugin manifest
  is `.codex-plugin/plugin.json`, identifying it as `dot-core` v0.0.4.
- The manifest declares paths to missing UI assets, and the repo's metadata
  validator does not recognize the manifest's `hooks` field. No test proves
  the loader contract or relative command working directory.
- `hooks.json` registers six events. Nineteen shell files exist; after
  excluding two private Stop children, eleven public event scripts are
  unwired.
- The shared `scripts/skogai-jq.sh` reads stdin and provides field, log, context,
  and decision helpers. Several active hooks bypass it and duplicate logging.
- It requires Bash, `jq`, and `date`. Log paths are built directly from
  unvalidated session IDs under `/tmp`.
- The logger calls its output JSONL, but plain `jq -n` emits pretty,
  multi-line objects. Its Bats test explicitly accepts a JSON stream rather
  than enforcing one JSON object per line.
- The same session file can contain both enriched envelopes and raw payloads.
- Marketplace scaffold/test tools are hardcoded to `skoghooks`; this plugin has
  no add/change/remove workflow.
- The real nested Bats invocation passes 116/116 tests, and the lesson matcher
  passes 36/36 Python tests. The documented `bats tests/*` command is a silent
  no-op in this tree.
- Those tests cover behavior, including some unwired scripts. They do not test
  manifest loading, registry drift, exact registered commands, strict JSONL,
  invalid input/path traversal, or concurrent appends.
- No CI runs them.

Useful idea: the envelope fields `timestamp`, observed event, session ID, and
raw input. Reimplement with the Python standard library rather than carrying
over the shell/jq dependency and mixed formats.

## Live verification performed

- `claude plugin validate ./plugins/skoghooks` passed with warnings that
  `hooks.description` and `hooks.events` are unknown and ignored.
- `claude plugin validate .` passed for the marketplace.
- The current `skoghooks` smoke runner produced 7/14 passing command
  invocations in a clean offline environment. Seven failed during unnecessary
  dependency resolution.
- `skogix-hooks` passed 116/116 Bats tests with the actual nested glob and
  36/36 lesson-matcher tests. Those results do not establish engine correctness.
- The worktree already contained deleted `.claude/hooks/state/*` files before
  this audit; they were left untouched.

## Missing engine contract

The current suites do not jointly prove any of the following:

- every host-supported event is registered exactly once;
- every registry entry invokes the intended recorder;
- every registered event has a fixture and unknown registry keys fail;
- one invocation appends exactly one parseable JSON object on exactly one line;
- the raw payload survives unchanged inside a versioned envelope;
- malformed input follows the chosen fail-open policy observably;
- output paths cannot escape through payload-controlled fields;
- simultaneous appends cannot interleave or corrupt records;
- plugin and marketplace manifests pass the real host validator;
- the contract is executed in CI.

## Smallest credible management workflow

This is an audit conclusion, not yet an approved implementation design.

1. Keep one authoritative supported-event list per host adapter.
2. Register every event to the same dependency-free recorder entrypoint.
3. Keep one representative raw fixture per supported event.
4. Parameterize one contract test from the registry; do not scaffold a new
   program per event.
5. Fail on unknown events, missing fixtures, duplicate registrations, missing
   commands, invalid output, or a record-count mismatch.
6. Run host manifest validation and the contract test in CI.
7. Add behavior dispatch only after a behavior has an explicit requirement and
   its own contract.

## Open decisions before design

- First host: Claude Code only, or Claude Code plus Codex immediately.
- Supported-event authority: checked-in host snapshot, generated host output,
  or a manually maintained registry verified against host documentation/CLI.
- Log destination and ownership: one project file, one user file, or an
  explicitly configured path.
- Failure semantics: fail open with a diagnostic sink, or fail visibly when
  recording itself fails.
- Raw-data policy: capture everything as requested, with later redaction and
  retention deliberately out of the MVP, or define exclusions now.

