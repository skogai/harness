"""skogharness CLI entry point."""

import os
from collections.abc import Sequence
from pathlib import Path

import click

from .install_skill import InstallResult, install_category, install_skills


def _find_repo_root(start: Path) -> Path:
    """Walk up from `start` looking for a `.git` directory; fall back to `start`."""
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


def _default_skills_target() -> Path:
    return _default_category_target("skills")


def _default_category_target(category: str) -> Path:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir) / ".claude" / category
    return _find_repo_root(Path.cwd()) / ".claude" / category


def _emit_results(results: Sequence[InstallResult]) -> None:
    if not results:
        click.echo("No files found to install.")
        return

    for result in results:
        prefix = "OK" if result.installed else "FAIL"
        click.echo(f"[{prefix}] {result.skill_name}: {result.message}")

    if any(not r.installed for r in results):
        raise SystemExit(1)


def _install_category_command(category: str, target: Path | None, dry_run: bool) -> None:
    resolved_target = target or _default_category_target(category)
    try:
        results = install_category(category, resolved_target, dry_run=dry_run)
    except ValueError as e:
        raise click.ClickException(str(e)) from e

    _emit_results(results)


@click.group()
def main():
    """skogharness — installs this repo's .claude/ content from source categories."""


@main.group()
def install():
    """Install a content category into a target .claude/ directory."""


@install.command("skills")
@click.option(
    "--target",
    type=click.Path(path_type=Path),
    default=None,
    help="Target skills directory (default: $CLAUDE_PROJECT_DIR/.claude/skills).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview what would be installed without writing anything.",
)
def install_skills_command(target: Path, dry_run: bool):
    """Copy every skill under src/skogharness/skills/ into the target directory."""
    target = target or _default_skills_target()
    try:
        results = install_skills(target, dry_run=dry_run)
    except ValueError as e:
        raise click.ClickException(str(e)) from e

    _emit_results(results)


@install.command("agents")
@click.option(
    "--target",
    type=click.Path(path_type=Path),
    default=None,
    help="Target category directory (default: $CLAUDE_PROJECT_DIR/.claude/agents).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview what would be installed without writing anything.",
)
def install_agents_command(target: Path | None, dry_run: bool) -> None:
    """Copy agent files into a target .claude/agents directory."""
    _install_category_command("agents", target, dry_run)


@install.command("commands")
@click.option(
    "--target",
    type=click.Path(path_type=Path),
    default=None,
    help="Target category directory (default: $CLAUDE_PROJECT_DIR/.claude/commands).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview what would be installed without writing anything.",
)
def install_commands_command(target: Path | None, dry_run: bool) -> None:
    """Copy command files into a target .claude/commands directory."""
    _install_category_command("commands", target, dry_run)


@install.command("hooks")
@click.option(
    "--target",
    type=click.Path(path_type=Path),
    default=None,
    help="Target category directory (default: $CLAUDE_PROJECT_DIR/.claude/hooks).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview what would be installed without writing anything.",
)
def install_hooks_command(target: Path | None, dry_run: bool) -> None:
    """Copy hook files into a target .claude/hooks directory."""
    _install_category_command("hooks", target, dry_run)


@install.command("mcp")
@click.option(
    "--target",
    type=click.Path(path_type=Path),
    default=None,
    help="Target category directory (default: $CLAUDE_PROJECT_DIR/.claude/mcp).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview what would be installed without writing anything.",
)
def install_mcp_command(target: Path | None, dry_run: bool) -> None:
    """Copy MCP files into a target .claude/mcp directory."""
    _install_category_command("mcp", target, dry_run)


@install.command("modes")
@click.option(
    "--target",
    type=click.Path(path_type=Path),
    default=None,
    help="Target category directory (default: $CLAUDE_PROJECT_DIR/.claude/modes).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview what would be installed without writing anything.",
)
def install_modes_command(target: Path | None, dry_run: bool) -> None:
    """Copy mode files into a target .claude/modes directory."""
    _install_category_command("modes", target, dry_run)


if __name__ == "__main__":
    main()
