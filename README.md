# Skills

Opinionated AI agent skills for Python, Django, and software development.

## Skills

| Skill | Description |
|-------|-------------|
| [python](skills/python/) | App architecture (entry points -> services -> data), functions (keyword-only args, docstrings), type hints (PEP 604), class naming, data structures (Pydantic over dicts), module organization |
| [django](skills/django/) | Models, views, admin, Celery task patterns, service provider pattern |
| [django-ninja](skills/django-ninja/) | Django Ninja routers, auth tiers, typed requests, Pydantic input/output models |
| [pytest](skills/pytest/) | AAA pattern, fixture organization, parametrize, Django database access, mock client testing, e2e test conventions |
| [copywriting](skills/copywriting/) | Natural voice guidelines, AI-tell word avoidance, email subject lines, formatting rules, outbound email voice |
| [docstore](skills/docstore/) | Document-collection data organization for semi-structured repositories, file placement conventions, collection-based directory structure |

## Install

### Via symlinks (recommended for development)

```bash
python scripts/install.py        # all skills
python scripts/install.py django  # specific skill
python scripts/install.py -f     # force overwrite
```

Creates symlinks in `~/.agents/skills/` and `~/.claude/skills/`.

### Manual

Copy a skill directory to your agent's skills location:

```bash
cp -r skills/django ~/.claude/skills/django
```

## Philosophy

These skills encode opinionated decisions that an LLM wouldn't make on its own:

- **Python**: layered architecture (entry points -> services -> data), keyword-only args for 4+ parameters, CamelCase abbreviations (JsonParser not JSONParser), Pydantic models over dicts, furl for URL parsing
- **Django**: EnumField over CharField with choices, service provider pattern with registry + factory, Celery task naming
- **Django Ninja**: two-tier auth (require_user vs session_auth), typed request annotations, Pydantic Input suffix convention
- **Pytest**: flat functions (no test classes), fixture discovery order, AAA with no empty sections, e2e marker convention
- **Copywriting**: specific AI-tell words to avoid, no em dashes, no rule-of-three, plain text emails

See [AGENTS.md](AGENTS.md) for the skill creation guide.

## Contributing

Each skill follows the three-tier progressive disclosure model:

1. **Frontmatter** (~100 tokens) — always loaded for trigger matching
2. **SKILL.md body** (<500 lines) — loaded when skill activates
3. **references/** (unlimited) — loaded on demand for specific topics

See [AGENTS.md](AGENTS.md) for full details on structure, writing patterns, and conventions.
