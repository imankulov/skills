# Skills

Opinionated AI agent skills for Python, Django, and software development.

## Skills

| Skill | Description |
|-------|-------------|
| [python](skills/python/) | App architecture (entry points -> services -> data), functions (keyword-only args, docstrings), type hints (PEP 604), class naming, data structures (Pydantic over dicts), module organization |
| [django](skills/django/) | Models, views, admin, Celery task patterns, service provider pattern |
| [django-ninja](skills/django-ninja/) | Django Ninja routers, auth tiers, typed requests, Pydantic input/output models |
| [pytest](skills/pytest/) | AAA pattern, fixture organization, parametrize, Django database access, mock client testing, e2e test conventions |
| [writing](skills/writing/) | Clear prose guidelines, Strunk's composition rules, AI-tell word avoidance, formatting, email voice |
| [draft](skills/draft/) | Draft any human-facing text (Slack messages, emails, proposals, summaries) — saves to a temp file and opens in VS Code |
| [docstore](skills/docstore/) | Document-collection data organization for semi-structured repositories, file placement conventions, collection-based directory structure |
| [screenshot-maker](skills/screenshot-maker/) | Documentation-ready screenshots with element targeting, blur, highlight (border/spotlight), and professional framing (rounded corners, shadows, gradient backgrounds) |
| [sessions](skills/sessions/) | List past Claude Code sessions for the current project — dates, turn counts, first message, session IDs |
| [dependency-cooldown](skills/dependency-cooldown/) | Configure minimum release age (default 7 days) for npm, pnpm, yarn, uv, pip at user or project level to defend against supply chain attacks |
| [editor-content](skills/editor-content/) | Reader-perspective content review — finds where prose drags, confuses, or loses the reader; flags AI tells, triplets, and overexplaining; reports a table of issues by default, or applies the fixes in-place when asked |
| [editor-copy](skills/editor-copy/) | In-place copy edit for grammar, style, and phrasing, applying the writing skill's guidelines without rewriting content or touching code |

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
