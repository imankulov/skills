#!/usr/bin/env python3
"""Uninstall skills symlinked by scripts/install.py."""

import argparse
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_DIR / "skills"
TARGETS = [
    Path.home() / ".agents" / "skills",
    Path.home() / ".claude" / "skills",
]


def find_skills(names: list[str] | None) -> list[Path]:
    """Find requested skill directories, or discover all skills."""
    if names:
        skills = []
        for name in names:
            skill_dir = SKILLS_DIR / name
            if not (skill_dir / "SKILL.md").exists():
                print(
                    f"error: '{name}' is not a skill (no SKILL.md found)",
                    file=sys.stderr,
                )
                raise SystemExit(1)
            skills.append(skill_dir)
        return skills

    return sorted(
        directory
        for directory in SKILLS_DIR.iterdir()
        if directory.is_dir() and (directory / "SKILL.md").exists()
    )


def uninstall_skill(skill: Path, target_dir: Path) -> str:
    """Remove a symlink when it points to the repository skill."""
    link = target_dir / skill.name
    if not link.is_symlink():
        return "not installed"
    if link.resolve() != skill.resolve():
        return "skipped: points elsewhere"

    link.unlink()
    return "removed"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove skill symlinks created by scripts/install.py."
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skill names to uninstall (default: all)",
    )
    args = parser.parse_args()

    skills = find_skills(args.skills or None)
    if not skills:
        print("No skills found.", file=sys.stderr)
        raise SystemExit(1)

    removed = 0
    for skill in skills:
        results = [uninstall_skill(skill, target_dir) for target_dir in TARGETS]
        removed += results.count("removed")
        print(f"  {skill.name}: {', '.join(results)}")

    print(f"\nRemoved {removed} symlink(s) from {', '.join(str(t) for t in TARGETS)}")


if __name__ == "__main__":
    main()
