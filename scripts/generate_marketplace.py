#!/usr/bin/env python3
"""Generate the Claude Code marketplace catalog from SKILL.md files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_DIR / "skills"
MARKETPLACE_PATH = REPO_DIR / ".claude-plugin" / "marketplace.json"

REPOSITORY = "https://github.com/imankulov/skills"
AUTHOR = {
    "name": "Roman Imankulov",
    "email": "roman.imankulov@gmail.com",
    "url": "https://github.com/imankulov",
}
MARKETPLACE_NAME = "imankulov-skills"


@dataclass(frozen=True)
class SkillMetadata:
    name: str
    description: str
    path: Path

    @property
    def short_description(self) -> str:
        match = re.search(r"(?<=[.!?])\s", self.description)
        if match:
            return self.description[: match.start()]
        return self.description

    @property
    def display_name(self) -> str:
        return self.name.replace("-", " ").title()

    @property
    def homepage(self) -> str:
        return f"{REPOSITORY}/tree/main/skills/{self.name}"

    @property
    def keywords(self) -> list[str]:
        return [*self.name.split("-"), "agent-skills"]


def parse_frontmatter(path: Path) -> SkillMetadata:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")

    try:
        closing_index = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path}: unclosed YAML frontmatter") from error

    frontmatter = lines[1:closing_index]
    name: str | None = None
    description: str | None = None

    for index, line in enumerate(frontmatter):
        if line.startswith("name:"):
            name = line.partition(":")[2].strip().strip("'\"")
        elif line.startswith("description:"):
            value = line.partition(":")[2].strip()
            if value in {"|", ">"}:
                description_lines: list[str] = []
                for continuation in frontmatter[index + 1 :]:
                    if continuation and not continuation[0].isspace():
                        break
                    description_lines.append(continuation.strip())
                description = " ".join(description_lines).strip()
            else:
                description = value.strip("'\"")

    if not name or not description:
        raise ValueError(f"{path}: frontmatter must define name and description")
    if name != path.parent.name:
        raise ValueError(
            f"{path}: frontmatter name {name!r} must match directory {path.parent.name!r}"
        )

    return SkillMetadata(name=name, description=description, path=path.parent)


def discover_skills() -> list[SkillMetadata]:
    return [
        parse_frontmatter(path)
        for path in sorted(SKILLS_DIR.glob("*/SKILL.md"))
    ]


def marketplace_manifest(skills: list[SkillMetadata]) -> dict[str, object]:
    plugins = []
    for skill in skills:
        plugins.append(
            {
                "name": skill.name,
                "displayName": skill.display_name,
                "source": "./",
                "skills": [f"./skills/{skill.name}"],
                "strict": False,
                "description": skill.short_description,
                "author": AUTHOR,
                "homepage": skill.homepage,
                "repository": REPOSITORY,
                "keywords": skill.keywords,
                "category": "development",
                "tags": skill.keywords,
            }
        )

    return {
        "name": MARKETPLACE_NAME,
        "owner": AUTHOR,
        "description": "Opinionated skills for Python, Django, writing, and software development.",
        "plugins": plugins,
    }


def serialized(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def expected_files(skills: list[SkillMetadata]) -> dict[Path, str]:
    return {MARKETPLACE_PATH: serialized(marketplace_manifest(skills))}


def legacy_plugin_manifests() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/.claude-plugin/plugin.json"))


def check_files(files: dict[Path, str]) -> bool:
    stale = [
        path.relative_to(REPO_DIR)
        for path, content in files.items()
        if not path.exists() or path.read_text(encoding="utf-8") != content
    ]
    stale.extend(path.relative_to(REPO_DIR) for path in legacy_plugin_manifests())
    if not stale:
        print("Claude marketplace metadata is up to date.")
        return True

    print("Claude marketplace metadata is stale:", file=sys.stderr)
    for path in stale:
        print(f"  {path}", file=sys.stderr)
    print(
        "Run: python scripts/generate_marketplace.py",
        file=sys.stderr,
    )
    return False


def write_files(files: dict[Path, str]) -> None:
    for path in legacy_plugin_manifests():
        path.unlink()
        path.parent.rmdir()
        print(f"removed {path.relative_to(REPO_DIR)}")

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path.relative_to(REPO_DIR)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Claude Code marketplace metadata from skills."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated metadata is missing or stale.",
    )
    args = parser.parse_args()

    try:
        files = expected_files(discover_skills())
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        return 0 if check_files(files) else 1

    write_files(files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
