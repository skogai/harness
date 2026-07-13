import re
from pathlib import Path

import pytest

from skogharness.cli.install_skill import install_skills, list_available_skills

LINK_PATTERN = re.compile(r"`((?:\.\./)*(?:references/)[\w.-]+\.md)`")


def _relative_links(skill_md: Path) -> list[str]:
    return LINK_PATTERN.findall(skill_md.read_text())


@pytest.mark.parametrize("skill_name", list_available_skills())
def test_installed_skill_relative_links_resolve(tmp_path, skill_name):
    target = tmp_path / ".claude" / "skills"
    install_skills(target)

    skill_md = target / skill_name / "SKILL.md"
    for link in _relative_links(skill_md):
        resolved = (skill_md.parent / link).resolve()
        assert resolved.exists(), f"{skill_name}/SKILL.md links to missing {link}"
