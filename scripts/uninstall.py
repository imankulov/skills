#!/usr/bin/env python3
"""Uninstall skills symlinked by scripts/install.py."""

import argparse
import sys
from pathlib import Path

from skill_paths import TARGETS, find_skills


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

    try:
        skills = find_skills(args.skills or None)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    if not skills:
        print("No skills found.", file=sys.stderr)
        raise SystemExit(1)

    removed = 0
    for skill in skills:
        results = [uninstall_skill(skill, target_dir) for target_dir in TARGETS]
        removed += results.count("removed")
        print(f"  {skill.name}: {', '.join(results)}")

    targets = ", ".join(str(target) for target in TARGETS)
    print(f"\nRemoved {removed} symlink(s) from {targets}")


if __name__ == "__main__":
    main()
