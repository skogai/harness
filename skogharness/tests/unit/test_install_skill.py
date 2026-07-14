from pathlib import Path
from collections.abc import Callable, Iterable

import pytest

from skogharness.cli.install_skill import (
    install_category,
    get_skills_source,
    install_skills,
    list_installable_categories,
    list_available_skills,
    resolve_target,
)


IgnoreFunction = Callable[[str, list[str]], Iterable[str]]
CopyFunction = Callable[[str, str], object]


def test_lists_all_skills():
    skills = list_available_skills()
    assert len(skills) == 10
    assert "harness-creator" in skills


def test_install_copies_all_skills(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "skills"
    results = install_skills(target)

    assert all(r.installed for r in results)
    for name in list_available_skills():
        assert (target / name / "SKILL.md").exists()


def test_lists_installable_categories():
    categories = list_installable_categories()

    assert categories == ["agents", "commands", "hooks", "mcp", "modes", "skills"]


def test_install_copies_non_skill_category(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "agents"
    results = install_category("agents", target)

    assert all(r.installed for r in results)
    assert (target / "example.md").exists()
    assert (target / "README.md").exists()


def test_install_category_dry_run_writes_nothing(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "commands"
    results = install_category("commands", target, dry_run=True)

    assert all(r.installed for r in results)
    assert not target.exists()


def test_install_category_rejects_unknown_category(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        _ = install_category("unknown", tmp_path / ".claude" / "unknown")


def test_install_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "skills"
    _ = install_skills(target)
    results = install_skills(target)

    assert all(r.installed for r in results)
    for name in list_available_skills():
        assert (target / name / "SKILL.md").exists()


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    target = tmp_path / ".claude" / "skills"
    results = install_skills(target, dry_run=True)

    assert all(r.installed for r in results)
    assert not target.exists()


def test_resolve_target_rejects_filesystem_root():
    with pytest.raises(ValueError):
        _ = resolve_target(Path("/"))


def test_resolve_target_rejects_source_overlap():
    source = get_skills_source()
    with pytest.raises(ValueError):
        _ = resolve_target(source)
    with pytest.raises(ValueError):
        _ = resolve_target(source / "harness-creator")
    with pytest.raises(ValueError):
        _ = resolve_target(source.parent)


def test_install_does_not_delete_source_on_overlap():
    source = get_skills_source()
    before = list_available_skills()
    with pytest.raises(ValueError):
        _ = install_skills(source)
    assert list_available_skills() == before
    for name in before:
        assert (source / name / "SKILL.md").exists()


def test_failed_copy_does_not_destroy_existing_install(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / ".claude" / "skills"
    _ = install_skills(target)

    skill_name = list_available_skills()[0]
    marker = target / skill_name / "SKILL.md"
    original_contents = marker.read_text()

    import shutil as shutil_module

    real_copytree = shutil_module.copytree

    def failing_copytree(
        src: str | Path,
        dst: str | Path,
        symlinks: bool = False,
        ignore: IgnoreFunction | None = None,
        copy_function: CopyFunction = shutil_module.copy2,
        ignore_dangling_symlinks: bool = False,
        dirs_exist_ok: bool = False,
    ) -> str | Path:
        if Path(src).name == skill_name:
            raise OSError("simulated copy failure")
        return real_copytree(
            src,
            dst,
            symlinks,
            ignore,
            copy_function,
            ignore_dangling_symlinks,
            dirs_exist_ok,
        )

    monkeypatch.setattr(
        "skogharness.cli.install_skill.shutil.copytree", failing_copytree
    )

    results = install_skills(target)
    failed = [r for r in results if r.skill_name == skill_name][0]

    assert not failed.installed
    assert marker.exists()
    assert marker.read_text() == original_contents
