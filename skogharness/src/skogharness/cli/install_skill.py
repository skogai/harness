"""
Skill installation command.

Copies every skill directory under src/skogharness/skills/ into a target
.claude/skills/ directory. Plain copy — no manifest, sync, or
managed-block tracking.
"""

import shutil
import uuid
from pathlib import Path
from typing import Final, NamedTuple


CATEGORY_NAMES: Final = ("agents", "commands", "hooks", "mcp", "modes", "skills")


class InstallResult(NamedTuple):
    skill_name: str
    installed: bool
    message: str


def get_skills_source() -> Path:
    """Directory containing this package's skill source directories."""
    return get_category_source("skills")


def get_package_source() -> Path:
    """Directory containing this package's installable source categories."""
    return Path(__file__).resolve().parent.parent


def get_category_source(category: str) -> Path:
    """Directory containing one installable source category."""
    if category not in CATEGORY_NAMES:
        raise ValueError(f"Unknown install category: {category}")
    return get_package_source() / category


def list_installable_categories() -> list[str]:
    return list(CATEGORY_NAMES)


def list_available_skills() -> list[str]:
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


def resolve_category_target(category: str, target: Path) -> Path:
    """Resolve a category target and reject source-tree overlap."""
    resolved = target.expanduser().resolve()
    cwd_root = Path.cwd().resolve().anchor
    if str(resolved) == cwd_root or resolved == Path(cwd_root):
        raise ValueError(f"Refusing to install into filesystem root: {resolved}")

    source = get_category_source(category).resolve()
    if resolved == source or source in resolved.parents or resolved in source.parents:
        raise ValueError(
            f"Refusing to install into the packaged {category} source tree: {resolved}"
        )
    return resolved


def _install_source_item(source_item: Path, item_target: Path) -> None:
    staging_target = item_target.with_name(
        f".{item_target.name}.staging-{uuid.uuid4().hex}"
    )
    item_target.parent.mkdir(parents=True, exist_ok=True)

    try:
        if source_item.is_dir():
            _ = shutil.copytree(source_item, staging_target)
        else:
            _ = shutil.copy2(source_item, staging_target)
    except OSError:
        if staging_target.is_dir():
            shutil.rmtree(staging_target, ignore_errors=True)
        elif staging_target.exists():
            staging_target.unlink()
        raise

    if item_target.is_dir():
        shutil.rmtree(item_target)
    elif item_target.exists():
        item_target.unlink()
    _ = staging_target.rename(item_target)


def install_category(
    category: str, target: Path, dry_run: bool = False
) -> list[InstallResult]:
    """Install an available category into target, overwriting existing copies."""
    if category == "skills":
        return install_skills(target, dry_run=dry_run)

    source = get_category_source(category)
    target = resolve_category_target(category, target)
    results: list[InstallResult] = []

    for source_item in sorted(source.iterdir()):
        item_target = target / source_item.name
        if dry_run:
            results.append(
                InstallResult(source_item.name, True, f"Would install to {item_target}")
            )
            continue

        try:
            _install_source_item(source_item, item_target)
        except OSError as e:
            results.append(InstallResult(source_item.name, False, f"Failed: {e}"))
            continue

        results.append(InstallResult(source_item.name, True, f"Installed to {item_target}"))

    return results


def install_skills(target: Path, dry_run: bool = False) -> list[InstallResult]:
    """Install every available skill into target, overwriting existing copies.

    Each skill is copied into a temporary sibling directory first; the live
    directory is only replaced once that copy succeeds, so a failed copy
    never leaves a skill partially written or missing.
    """
    source = get_skills_source()
    target = resolve_target(target)
    results: list[InstallResult] = []

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
            _ = shutil.copytree(skill_source, staging_target)
        except OSError as e:
            shutil.rmtree(staging_target, ignore_errors=True)
            results.append(InstallResult(skill_name, False, f"Failed: {e}"))
            continue

        if skill_target.exists():
            shutil.rmtree(skill_target)
        _ = staging_target.rename(skill_target)
        results.append(InstallResult(skill_name, True, f"Installed to {skill_target}"))

    return results
