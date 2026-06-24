# Opinionated agent skills

Reusable skills for Claude Code, Codex, Cursor, and other compatible agents. They
define choices that general framework documentation leaves open, including layered
Python architecture, EnumField-based Django models, and direct prose without common
AI writing patterns.

## Install with `npx skills`

This method requires Node.js and npm. Install all skills globally to make them
available in every project:

```bash
npx skills add imankulov/skills -g
```

Run `npx skills add imankulov/skills --list` to view the available skills before
installation.

## Available skills

| Category | Skill | Description |
|----------|-------|-------------|
| Python | [python](skills/python/) | Structure type-safe Python applications with layered architecture and explicit data models |
| Python | [django](skills/django/) | Build maintainable Django models, views, admin tools, tasks, and service integrations |
| Python | [django-ninja](skills/django-ninja/) | Create typed Django Ninja APIs with consistent routing and authentication |
| Python | [pytest](skills/pytest/) | Write flat, readable pytest tests using AAA, fixtures, and parametrization |
| Writing | [writing](skills/writing/) | Write direct, human-sounding prose without common AI patterns |
| Writing | [draft](skills/draft/) | Draft human-facing text in a temporary file for review |
| Writing | [editor-content](skills/editor-content/) | Review prose for engagement, clarity, structure, and AI writing patterns |
| Writing | [editor-copy](skills/editor-copy/) | Apply grammar, style, and phrasing fixes without changing the content's substance |
| Tools | [docstore](skills/docstore/) | Organize semi-structured document repositories into predictable collections |
| Tools | [screenshot-maker](skills/screenshot-maker/) | Produce framed documentation screenshots with targeting and redaction controls |
| Tools | [sessions](skills/sessions/) | Find and inspect past Claude Code sessions for the current project |
| Security | [dependency-cooldown](skills/dependency-cooldown/) | Block newly released package versions during a configurable safety period |

Install selected skills:

```bash
npx skills add imankulov/skills -g --skill django --skill pytest
```

Omit `-g` to install into the current project. Use `-a` to target specific agents:

```bash
npx skills add imankulov/skills -g -a claude-code -a codex
```

## Install from the Claude Code marketplace

Run these commands in a Claude Code session. First, add this repository as a
marketplace:

```text
/plugin marketplace add imankulov/skills
```

Then install a skill as a Claude Code plugin:

```text
/plugin install django@imankulov-skills
```

The names in this example map as follows:

```text
marketplace: imankulov-skills
plugin:      django
skill:       django
command:     /django:django
```

Replace `django` with any skill name from the table above. Claude Code invokes plugin
skills as `/plugin-name:skill-name`; the marketplace name appears only during
installation. If you install a plugin during an existing session, run
`/reload-plugins` before using it.

## Development installation

Clone the repository, then create symlinks so edits take effect immediately:

```bash
git clone https://github.com/imankulov/skills.git
cd skills
python scripts/install.py
```

The installer links every skill into `~/.agents/skills/` and `~/.claude/skills/`.
Pass skill names to install a subset, or use `-f` to replace existing installations:

```bash
python scripts/install.py django pytest
python scripts/install.py -f
```

Remove selected skills or all skills installed from this checkout:

```bash
python scripts/uninstall.py django pytest
python scripts/uninstall.py
```

The uninstaller removes only symlinks that point to this repository. It leaves copied
skills, regular directories, and symlinks to other checkouts unchanged.

## Contributing

To add a skill:

1. Create `skills/<name>/SKILL.md` with matching `name` and `description` frontmatter.
2. Add any supporting files under `references/` or `scripts/`.
3. Run `python scripts/generate_marketplace.py`.
4. Run `pre-commit run --all-files`.

Install [pre-commit](https://pre-commit.com/) and enable the repository hook before
committing:

```bash
python -m pip install pre-commit
pre-commit install
```

The hook regenerates `.claude-plugin/marketplace.json` from each skill's frontmatter.
The `skills/` directory remains the source of truth, and individual skill directories
don't contain separate plugin manifests. Run the generator after adding or renaming a
skill:

```bash
python scripts/generate_marketplace.py
python scripts/generate_marketplace.py --check
```

### Marketplace design

The marketplace maps each skill to a separate plugin so users can install `django`
without also installing `python` or `pytest`. This creates more marketplace entries
and repeated names such as `/django:django`.

Claude Code plugins can contain several related skills under one namespace. Grouped
plugins can be added later without changing the canonical directories under `skills/`.

### Skill structure

Each skill follows the three-tier progressive disclosure model:

1. **Frontmatter** (~100 tokens) — always loaded for trigger matching
2. **SKILL.md body** (<500 lines) — loaded when skill activates
3. **references/** (unlimited) — loaded on demand for specific topics

See [AGENTS.md](AGENTS.md) for details on structure, writing patterns, and conventions.
