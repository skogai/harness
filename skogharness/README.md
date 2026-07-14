# skogharness

Installer package for this repo's `.claude/` content. Source content lives
under `src/skogharness/<category>/` (skills, agents, commands, hooks, modes,
mcp); `skogharness install <category>` copies it into a target `.claude/`
directory.

No manifest, sync, status, or drift-detection mechanism — installs are
plain copies you re-run when source content changes.

## Usage

```sh
mise run test:skogharness
uv run skogharness install skills [--target DIR] [--dry-run]
uv run skogharness install agents [--target DIR] [--dry-run]
uv run skogharness install commands [--target DIR] [--dry-run]
uv run skogharness install hooks [--target DIR] [--dry-run]
uv run skogharness install modes [--target DIR] [--dry-run]
uv run skogharness install mcp [--target DIR] [--dry-run]
```

Defaults to installing into `$CLAUDE_PROJECT_DIR/.claude/<category>` (falling
back to `<repo-root>/.claude/<category>` when unset).

Only `skills` contains production skills today. The other categories are a
basic framework shell and are safe to install as examples; they do not activate
runtime hooks, MCP servers, or agent routing by themselves.
