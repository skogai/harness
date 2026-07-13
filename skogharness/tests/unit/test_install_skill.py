from pathlib import Path

import pytest

from skogharness.cli.install_skill import (
    get_skills_source,
    install_skills,
    list_available_skills,
    resolve_target,
)


def test_lists_all_nine_skills():
    skills = list_available_skills()
    assert len(skills) == 10
    assert "harness-creator" in skills


def test_install_copies_all_skills(tmp_path):
    target = tmp_path / ".claude" / "skills"
    results = install_skills(target)

    assert all(r.installed for r in results)
    for name in list_available_skills():
        assert (target / name / "SKILL.md").exists()


def test_install_is_idempotent(tmp_path):
    target = tmp_path / ".claude" / "skills"
    install_skills(target)
    results = install_skills(target)

    assert all(r.installed for r in results)
    for name in list_available_skills():
        assert (target / name / "SKILL.md").exists()


def test_dry_run_writes_nothing(tmp_path):
    target = tmp_path / ".claude" / "skills"
    results = install_skills(target, dry_run=True)

    assert all(r.installed for r in results)
    assert not target.exists()


def test_resolve_target_rejects_filesystem_root():
    with pytest.raises(ValueError):
        resolve_target(Path("/"))


def test_resolve_target_rejects_source_overlap():
    source = get_skills_source()
    with pytest.raises(ValueError):
        resolve_target(source)
    with pytest.raises(ValueError):
        resolve_target(source / "harness-creator")
    with pytest.raises(ValueError):
        resolve_target(source.parent)


def test_install_does_not_delete_source_on_overlap():
    source = get_skills_source()
    before = list_available_skills()
    with pytest.raises(ValueError):
        install_skills(source)
    assert list_available_skills() == before
    for name in before:
        assert (source / name / "SKILL.md").exists()


def test_failed_copy_does_not_destroy_existing_install(tmp_path, monkeypatch):
    target = tmp_path / ".claude" / "skills"
    install_skills(target)

    skill_name = list_available_skills()[0]
    marker = target / skill_name / "SKILL.md"
    original_contents = marker.read_text()

    import shutil as shutil_module

    real_copytree = shutil_module.copytree

    def failing_copytree(src, dst, *args, **kwargs):
        if Path(src).name == skill_name:
            raise OSError("simulated copy failure")
        return real_copytree(src, dst, *args, **kwargs)

    monkeypatch.setattr(
        "skogharness.cli.install_skill.shutil.copytree", failing_copytree
    )

    results = install_skills(target)
    failed = [r for r in results if r.skill_name == skill_name][0]

    assert not failed.installed
    assert marker.exists()
    assert marker.read_text() == original_contents
