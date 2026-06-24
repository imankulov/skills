"""Shared paths and skill discovery for local installation scripts."""

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
                raise ValueError(f"'{name}' is not a skill (no SKILL.md found)")
            skills.append(skill_dir)
        return skills

    return sorted(
        directory
        for directory in SKILLS_DIR.iterdir()
        if directory.is_dir() and (directory / "SKILL.md").exists()
    )
