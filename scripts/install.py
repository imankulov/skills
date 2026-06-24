#!/usr/bin/env python3
"""Install skills by creating symlinks in ~/.agents/skills and ~/.claude/skills."""

import argparse
import os
import sys
from pathlib import Path

from skill_paths import TARGETS, find_skills


def confirm(msg: str) -> bool:
    try:
        return input(f"{msg} [y/N] ").strip().lower() in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def install_skill(skill: Path, target_dir: Path, force: bool) -> bool:
    """Create a symlink target_dir/<name> -> skill. Returns True if installed."""
    target_dir.mkdir(parents=True, exist_ok=True)
    link = target_dir / skill.name

    if link.exists() or link.is_symlink():
        if link.is_symlink() and link.resolve() == skill.resolve():
            return True  # already correct
        if not link.is_symlink():
            print(
                f"  skipped: {link} exists and is not a symlink",
                file=sys.stderr,
            )
            return False

        if not force:
            if not confirm(
                f"  {link} already exists (symlink -> {os.readlink(link)}). Replace?"
            ):
                return False
        link.unlink()

    link.symlink_to(skill)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Install skills as symlinks.")
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skill names to install (default: all)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Replace existing symlinks without asking",
    )
    args = parser.parse_args()

    try:
        skills = find_skills(args.skills or None)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error
    if not skills:
        print("No skills found.", file=sys.stderr)
        sys.exit(1)

    for skill in skills:
        results = []
        for target_dir in TARGETS:
            installed = install_skill(skill, target_dir, args.force)
            results.append(("ok" if installed else "skipped", target_dir / skill.name))
        status = "ok" if any(r[0] == "ok" for r in results) else "skipped"
        print(f"  {status}: {skill.name}")

    targets = ", ".join(str(target) for target in TARGETS)
    print(f"\nInstalled {len(skills)} skill(s) to {targets}")


if __name__ == "__main__":
    main()
