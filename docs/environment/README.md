# Environments

Each file in this directory documents one runtime environment a Claude Code
session can run in when driving this repo. This `docs/` directory is distinct
from `.docs/` (the consolidated harness documentation).

Three environment variables identify an environment:

- `SKOGAI_MODE`
- `SKOGAI_ENVIRONMENT`
- `SKOGAI_CONFIG_DIR`

| Environment | `SKOGAI_MODE` | `SKOGAI_ENVIRONMENT` | `SKOGAI_CONFIG_DIR` |
| --- | --- | --- | --- |
| [claude-desktop](claude-desktop.md) | not set | not set | not set |
| [remote-control](remote-control.md) | not set | not set | `/home/skogix/skogai/config` |
| [remote-anthropic](remote-anthropic.md) | `cloud` | `remote` | `.skogai/config` |
