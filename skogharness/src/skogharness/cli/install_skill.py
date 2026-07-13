"""
Skill installation command.

Copies every skill directory under src/skogharness/skills/ into a target
.claude/skills/ directory. Plain copy — no manifest, sync, or
managed-block tracking.
"""

import shutil
import uuid
from pathlib import Path
from typing import List, NamedTuple


class InstallResult(NamedTuple):
    skill_name: str
    installed: bool
    message: str


def get_skills_source() -> Path:
    """Directory containing this package's skill source directories."""
    return Path(__file__).resolve().parent.parent / "skills"


def list_available_skills() -> List[str]:
    source = get_skills_source()
    if not source.exists():
        return []
    return sorted(
        item.name
        for item in source.iterdir()
        if item.is_dir() and (item / "SKILL.md").exists()
    )


def resolve_target(target: Path) -> Path:
    """Resolve and validate a target skills directory.

    Refuses the filesystem root, and refuses any target that overlaps the
    packaged skill source tree (as itself, an ancestor, or a descendant) so
    an install can never delete or corrupt the canonical source it copies
    from.
    """
    resolved = target.expanduser().resolve()
    cwd_root = Path.cwd().resolve().anchor
    if str(resolved) == cwd_root or resolved == Path(cwd_root):
        raise ValueError(f"Refusing to install into filesystem root: {resolved}")

    source = get_skills_source().resolve()
    if resolved == source or source in resolved.parents or resolved in source.parents:
        raise ValueError(
            f"Refusing to install into the packaged skill source tree: {resolved}"
        )
    return resolved


def install_skills(target: Path, dry_run: bool = False) -> List[InstallResult]:
    """Install every available skill into target, overwriting existing copies.

    Each skill is copied into a temporary sibling directory first; the live
    directory is only replaced once that copy succeeds, so a failed copy
    never leaves a skill partially written or missing.
    """
    source = get_skills_source()
    target = resolve_target(target)
    results: List[InstallResult] = []

    for skill_name in list_available_skills():
        skill_source = source / skill_name
        skill_target = target / skill_name

        if dry_run:
            results.append(
                InstallResult(skill_name, True, f"Would install to {skill_target}")
            )
            continue

        target.mkdir(parents=True, exist_ok=True)
        staging_target = target / f".{skill_name}.staging-{uuid.uuid4().hex}"
        try:
            shutil.copytree(skill_source, staging_target)
        except OSError as e:
            shutil.rmtree(staging_target, ignore_errors=True)
            results.append(InstallResult(skill_name, False, f"Failed: {e}"))
            continue

        if skill_target.exists():
            shutil.rmtree(skill_target)
        staging_target.rename(skill_target)
        results.append(InstallResult(skill_name, True, f"Installed to {skill_target}"))

    return results
