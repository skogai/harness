from click.testing import CliRunner
from pathlib import Path

from skogharness.cli.main import main


def test_cli_installs_non_skill_category_with_dry_run(tmp_path: Path) -> None:
    runner = CliRunner()
    target = tmp_path / ".claude" / "agents"

    result = runner.invoke(main, ["install", "agents", "--target", str(target), "--dry-run"])

    assert result.exit_code == 0
    assert "Would install" in result.output
    assert not target.exists()


def test_cli_installs_non_skill_category(tmp_path: Path) -> None:
    runner = CliRunner()
    target = tmp_path / ".claude" / "commands"

    result = runner.invoke(main, ["install", "commands", "--target", str(target)])

    assert result.exit_code == 0
    assert (target / "example.md").exists()
