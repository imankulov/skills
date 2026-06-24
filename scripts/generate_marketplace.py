#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pyyaml>=6.0.2,<7",
# ]
# ///
"""Generate repository catalogs from SKILL.md files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_DIR / "skills"
MARKETPLACE_PATH = REPO_DIR / ".claude-plugin" / "marketplace.json"
SKILLS_SH_PATH = REPO_DIR / "skills.sh.json"
SKILLS_SH_GROUPS_PATH = REPO_DIR / "skills.sh.groups.yaml"

REPOSITORY = "https://github.com/imankulov/skills"
AUTHOR = {
    "name": "Roman Imankulov",
    "email": "roman.imankulov@gmail.com",
    "url": "https://github.com/imankulov",
}
MARKETPLACE_NAME = "imankulov-skills"
SKILLS_SH_SCHEMA = "https://skills.sh/schemas/skills.sh.schema.json"
METADATA_PREFIX = "imankulov."


@dataclass(frozen=True)
class SkillMetadata:
    name: str
    description: str
    metadata: dict[str, str]
    path: Path

    @property
    def short_description(self) -> str:
        match = re.search(r"(?<=[.!?])\s", self.description)
        if match:
            return self.description[: match.start()]
        return self.description

    @property
    def display_name(self) -> str:
        return self.metadata_value(
            "claude-display-name",
            default=self.name.replace("-", " ").title(),
        )

    @property
    def homepage(self) -> str:
        return f"{REPOSITORY}/tree/main/skills/{self.name}"

    @property
    def keywords(self) -> list[str]:
        default = ",".join([*self.name.split("-"), "agent-skills"])
        value = self.metadata_value("claude-keywords", default=default)
        return [keyword.strip() for keyword in value.split(",") if keyword.strip()]

    @property
    def category(self) -> str:
        return self.metadata_value("claude-category", default="development")

    @property
    def skills_sh_group(self) -> str | None:
        return self.metadata.get(f"{METADATA_PREFIX}skills-sh-group")

    @property
    def skills_sh_order(self) -> int:
        return self.metadata_int("skills-sh-order", default=100)

    def metadata_value(self, key: str, *, default: str) -> str:
        return self.metadata.get(f"{METADATA_PREFIX}{key}", default)

    def metadata_int(self, key: str, *, default: int) -> int:
        value = self.metadata.get(f"{METADATA_PREFIX}{key}")
        if value is None:
            return default
        try:
            return int(value)
        except ValueError as error:
            raise ValueError(
                f"{self.path / 'SKILL.md'}: metadata {METADATA_PREFIX}{key} "
                f"must be an integer string"
            ) from error


@dataclass(frozen=True)
class SkillsShGroup:
    title: str
    description: str | None


def parse_frontmatter(path: Path) -> SkillMetadata:
    content = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", content, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"{path}: invalid YAML frontmatter: {error}") from error

    if not isinstance(frontmatter, dict):
        raise ValueError(f"{path}: frontmatter must be a YAML mapping")

    name = frontmatter.get("name")
    description = frontmatter.get("description")
    metadata = frontmatter.get("metadata", {})

    if not isinstance(name, str) or not isinstance(description, str):
        raise ValueError(f"{path}: frontmatter must define name and description")
    if not isinstance(metadata, dict) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in metadata.items()
    ):
        raise ValueError(f"{path}: metadata must map string keys to string values")
    if name != path.parent.name:
        raise ValueError(
            f"{path}: frontmatter name {name!r} must match directory {path.parent.name!r}"
        )

    return SkillMetadata(
        name=name,
        description=" ".join(description.split()),
        metadata=metadata,
        path=path.parent,
    )


def discover_skills() -> list[SkillMetadata]:
    return [
        parse_frontmatter(path)
        for path in sorted(SKILLS_DIR.glob("*/SKILL.md"))
    ]


def load_skills_sh_groups() -> list[SkillsShGroup]:
    try:
        config = yaml.safe_load(SKILLS_SH_GROUPS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"{SKILLS_SH_GROUPS_PATH}: file not found") from error
    except yaml.YAMLError as error:
        raise ValueError(
            f"{SKILLS_SH_GROUPS_PATH}: invalid YAML: {error}"
        ) from error

    if not isinstance(config, dict) or not isinstance(config.get("groups"), list):
        raise ValueError(f"{SKILLS_SH_GROUPS_PATH}: must contain a groups list")
    unknown_config_keys = sorted(set(config) - {"groups"})
    if unknown_config_keys:
        raise ValueError(
            f"{SKILLS_SH_GROUPS_PATH}: unknown keys: "
            + ", ".join(unknown_config_keys)
        )

    groups = []
    for index, item in enumerate(config["groups"]):
        if not isinstance(item, dict):
            raise ValueError(
                f"{SKILLS_SH_GROUPS_PATH}: groups[{index}] must be a mapping"
            )
        unknown_group_keys = sorted(set(item) - {"title", "description"})
        if unknown_group_keys:
            raise ValueError(
                f"{SKILLS_SH_GROUPS_PATH}: groups[{index}] has unknown keys: "
                + ", ".join(unknown_group_keys)
            )

        title = item.get("title")
        description = item.get("description")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(
                f"{SKILLS_SH_GROUPS_PATH}: groups[{index}].title must be a string"
            )
        if description is not None and not isinstance(description, str):
            raise ValueError(
                f"{SKILLS_SH_GROUPS_PATH}: groups[{index}].description must be a string"
            )

        groups.append(
            SkillsShGroup(
                title=title.strip(),
                description=description.strip() if description else None,
            )
        )

    titles = [group.title for group in groups]
    duplicates = sorted(
        title for title, count in Counter(titles).items() if count > 1
    )
    if duplicates:
        raise ValueError(
            f"{SKILLS_SH_GROUPS_PATH}: duplicate groups: {', '.join(duplicates)}"
        )
    if not groups:
        raise ValueError(f"{SKILLS_SH_GROUPS_PATH}: define at least one group")

    return groups


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
                "category": skill.category,
                "tags": skill.keywords,
            }
        )

    return {
        "name": MARKETPLACE_NAME,
        "owner": AUTHOR,
        "description": "Opinionated skills for Python, Django, writing, and software development.",
        "plugins": plugins,
    }


def skills_sh_manifest(
    skills: list[SkillMetadata],
    groups: list[SkillsShGroup],
) -> dict[str, object]:
    known_groups = {group.title for group in groups}
    unknown_groups = sorted(
        {
            skill.skills_sh_group
            for skill in skills
            if skill.skills_sh_group is not None
            and skill.skills_sh_group not in known_groups
        }
    )
    if unknown_groups:
        raise ValueError(
            "skill metadata references unknown skills.sh groups: "
            + ", ".join(unknown_groups)
        )

    groupings = []
    for group in groups:
        group_skills = [
            skill for skill in skills if skill.skills_sh_group == group.title
        ]
        if not group_skills:
            raise ValueError(
                f"{SKILLS_SH_GROUPS_PATH}: group {group.title!r} has no skills"
            )

        grouping: dict[str, object] = {
            "title": group.title,
            "skills": [
                skill.name
                for skill in sorted(
                    group_skills,
                    key=lambda skill: (skill.skills_sh_order, skill.name),
                )
            ],
        }
        if group.description:
            grouping["description"] = group.description
        groupings.append(grouping)

    return {
        "$schema": SKILLS_SH_SCHEMA,
        "notGrouped": "bottom",
        "groupings": groupings,
    }


def serialized(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def expected_files(
    skills: list[SkillMetadata],
    groups: list[SkillsShGroup],
) -> dict[Path, str]:
    return {
        MARKETPLACE_PATH: serialized(marketplace_manifest(skills)),
        SKILLS_SH_PATH: serialized(skills_sh_manifest(skills, groups)),
    }


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
        print("Generated repository metadata is up to date.")
        return True

    print("Generated repository metadata is stale:", file=sys.stderr)
    for path in stale:
        print(f"  {path}", file=sys.stderr)
    print(
        "Run: uv run scripts/generate_marketplace.py",
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
        description="Generate Claude Code and skills.sh metadata from skills."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if generated metadata is missing or stale.",
    )
    args = parser.parse_args()

    try:
        files = expected_files(discover_skills(), load_skills_sh_groups())
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        return 0 if check_files(files) else 1

    write_files(files)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
