#!/usr/bin/env python3
"""Install skills by creating symlinks in ~/.agents/skills and ~/.claude/skills."""

import argparse
import os
import sys
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_DIR / "skills"
TARGETS = [
    Path.home() / ".agents" / "skills",
    Path.home() / ".claude" / "skills",
]


def find_skills(names: list[str] | None) -> list[Path]:
    """Find skill directories in the repo. If names given, use those; otherwise discover all."""
    if names:
        skills = []
        for name in names:
            skill_dir = SKILLS_DIR / name
            if not (skill_dir / "SKILL.md").exists():
                print(f"error: '{name}' is not a skill (no SKILL.md found)", file=sys.stderr)
                sys.exit(1)
            skills.append(skill_dir)
        return skills
    return sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


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
        kind = "symlink" if link.is_symlink() else "directory"
        if not force:
            existing = f" -> {os.readlink(link)}" if link.is_symlink() else ""
            if not confirm(f"  {link} already exists ({kind}{existing}). Replace?"):
                return False
        if link.is_dir() and not link.is_symlink():
            import shutil
            shutil.rmtree(link)
        else:
            link.unlink()

    link.symlink_to(skill)
    return True


def main():
    parser = argparse.ArgumentParser(description="Install skills as symlinks.")
    parser.add_argument("skills", nargs="*", help="Skill names to install (default: all)")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing without asking")
    args = parser.parse_args()

    skills = find_skills(args.skills or None)
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

    print(f"\nInstalled {len(skills)} skill(s) to {', '.join(str(t) for t in TARGETS)}")


if __name__ == "__main__":
    main()
