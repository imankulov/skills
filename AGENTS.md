# Contributing Skills

This document defines how skills in this repository are structured, written, and
maintained. Follow it when creating new skills or modifying existing ones.

## Skill Architecture

Each skill is a directory under `skills/` with a required `SKILL.md` and optional
supporting files:

```
skills/my-skill/
├── SKILL.md              # Required: frontmatter + instructions
├── references/           # Optional: deep-dive docs loaded on demand
│   ├── topic-a.md
│   └── topic-b.md
└── scripts/              # Optional: executable helpers
    └── helper.py
```

Claude Code plugins are defined centrally in `.claude-plugin/marketplace.json`.
Do not add `.claude-plugin/plugin.json` inside individual skill directories. The
marketplace generator exposes each `skills/<name>` directory as a separate plugin
while keeping `SKILL.md` as the source of truth.

## The Three-Tier Progressive Disclosure Model

Skills load content in three tiers to conserve context window:

| Tier | What | Size Target | When Loaded |
|------|------|-------------|-------------|
| **Frontmatter** | `name` + `description` | ~100 tokens | Always in context — used for trigger matching |
| **SKILL.md body** | Core instructions, key patterns, reference pointers | <500 lines | When skill triggers |
| **references/** | Detailed rules, examples, checklists | Unlimited | When agent needs a specific topic |

The SKILL.md body is the "index + essentials." It should contain enough to handle
common cases without loading references, and clearly point to references for deep dives.

## SKILL.md Format

### Frontmatter

```yaml
---
name: my-skill
description: |
  What this skill does and when to use it. Also use when [related triggers].
  Do NOT use for: [explicit exclusions to prevent false matches].
metadata:
  imankulov.skills-sh-group: Python
  imankulov.skills-sh-order: "10"
  imankulov.claude-display-name: My Skill
  imankulov.claude-category: development
  imankulov.claude-keywords: "python,testing,agent-skills"
---
```

**name**: kebab-case, 1-64 characters, must match the directory name.

**description**: The single most important field. This is the ONLY thing the agent sees
when deciding whether to activate the skill. Write it to trigger correctly:

- Lead with what the skill does
- Include natural-language trigger phrases ("Use when writing...", "Also use when...")
- Add explicit negative triggers ("Do NOT use for: ...") to prevent false matches
- Be "pushy" — Claude undertriggers skills by default, so descriptions should lean
  toward broad matching rather than narrow

Good description:
```yaml
description: |
  Opinionated Django development patterns. Use when writing Django models, views,
  API endpoints, admin configuration, Celery tasks, or service layers.
  Also use when reviewing or refactoring Django code.
  Do NOT use for: FastAPI, Flask, general Python, or frontend code.
```

Bad description:
```yaml
description: Django patterns and best practices.
```

**metadata**: Optional string-to-string values used by repository integrations. Keep
keys flat and namespaced because the Agent Skills specification does not permit nested
metadata values.

| Key | Purpose | Default |
|-----|---------|---------|
| `imankulov.skills-sh-group` | Group title from `skills.sh.groups.yaml` | Ungrouped |
| `imankulov.skills-sh-order` | Numeric sort order within the group | `"100"` |
| `imankulov.claude-display-name` | Claude marketplace display name | Title-cased skill name |
| `imankulov.claude-category` | Claude marketplace category | `development` |
| `imankulov.claude-keywords` | Comma-separated marketplace keywords and tags | Skill-name parts plus `agent-skills` |

Group titles, descriptions, and display order live only in `skills.sh.groups.yaml`.
The order of entries in that file determines the group display order. A skill declares
only its group membership and optional within-group order. Omit
`imankulov.skills-sh-group` to show it under “Other skills” on skills.sh.

### Body Structure

The body should follow this order:

1. **Title and one-line summary** — what this skill teaches
2. **Core rules** — the essential knowledge (the part worth loading every time), each stated
   once, with any trap warning inline next to the rule it guards (see the Trap Test)
3. **Reference pointers** — links to `references/*.md` for deep dives

Optionally close with a verification checklist, but only if it adds checks the rules don't.

## Writing Patterns

Favor lean prompts. State each instruction once, positively — modern models follow a clear
positive rule better than a wall of wrong/right pairs.

### State Each Rule Once

State the rule as "do X" and stop:

```markdown
Use keyword-only arguments for functions with 4+ parameters.
```

If a line adds no information the rules above lack, cut it.

### The Trap Test — when a "don't Y" earns its place

Default to "do X." A "don't Y" earns a line only when it isn't a redundant mirror of one:

- **Drop it** if "do X" already rules Y out — pick `EnumField` and `CharField(choices=)` is
  off the table.
- **Keep it** if Y stays reachable despite X — usually the framework's or model's *default*
  is Y (`auto_now` silently skips on `.update()`; the reflex email opener "I hope this message
  finds you well").
- **Prefer it** when the negative is sharper — "don't add `max_length` to a Postgres
  `CharField`" pinpoints the habit that "keep fields unconstrained" blurs.

Keep the warning to one compact line beside the rule it guards.

### Examples

Add a code example only when the pattern can't be conveyed in one line of prose, or when
the exact shape is the point. Show the positive form alone; reach for a paired bad example
only when the trap test calls for showing the wrong path. Keep examples minimal — show the
pattern, not a full implementation.

### Verification Checklists

A checklist earns its place only if its items add checks not already stated as rules. Delete
one that restates the skill line-by-line.

### Reference Pointers

Link to references with context about when to load them:

```markdown
## References

- [Model standards](references/models.md) — base classes, EnumField, Meta
- [Service provider pattern](references/service-provider.md) — external integrations
```

The agent reads these only when the task requires that specific topic.

## What Makes a Good Skill

**Good Skill = Expert-only Knowledge minus What Claude Already Knows**

Focus on:

- **Opinionated decisions** that an LLM wouldn't make unprompted (e.g., "use keyword-only
  args for 4+ parameters")
- **Project conventions** that differ from framework defaults (e.g., "EnumField instead
  of CharField with choices")
- **Traps** specific to your stack that Claude would otherwise fall into — but only those a
  positive rule can't make unreachable (see the Trap Test)

Avoid:

- Restating framework documentation (Claude already knows Django model basics)
- Overly generic advice ("write clean code", "use meaningful variable names")
- Implementation details that belong in the codebase, not instructions

## Skill Sizing Guide

| Skill Size | When Appropriate |
|------------|-----------------|
| Small (<100 lines, no refs) | Single focused topic (e.g., URL parsing, class naming) |
| Medium (100-300 lines, 1-3 refs) | One framework area (e.g., pytest patterns) |
| Large (200-500 lines, 5+ refs) | Full framework coverage (e.g., Django skill) |

Don't exceed 500 lines in SKILL.md — move detail to references. Don't create skills
smaller than ~50 lines — they're better as references within a larger skill.

## De-Projectifying Rules into Skills

When extracting project-specific rules into shareable skills:

1. **Replace project-specific imports** with generic equivalents
   - `from myproject.utils import FrozenApiModel` -> `from pydantic import BaseModel, ConfigDict`
   - `from myproject.auth import require_user` -> describe the pattern generically

2. **Replace project-specific base classes** with definitions
   - Don't reference `MutableDjangoModel` — show how to create it
   - Don't reference `AuthRequestFactory` — describe the concept

3. **Generalize examples** — use `myapp`, `User`, `Order` instead of domain-specific names

4. **Keep the opinions** — the value is in the opinionated choices, not the specific
   implementation. "Use EnumField instead of CharField with choices" is shareable even
   if the import path changes.

5. **Remove project-specific file paths** — no references to specific conftest fixtures
   or gold standard files in someone else's codebase

## Installation

Skills are installed via symlinks using `scripts/install.py`:

```bash
# Install all skills
python scripts/install.py

# Install specific skills
python scripts/install.py django pytest

# Replace existing symlinks without prompting
python scripts/install.py -f
```

This creates symlinks in `~/.agents/skills/` and `~/.claude/skills/`, so updates
to the repo are immediately reflected. The installer never replaces regular files or
directories, even with `-f`.

## Generated repository metadata

After adding, renaming, or removing a skill, regenerate the repository catalogs:

```bash
uv run scripts/generate_marketplace.py
```

The generator reads each skill's `name`, `description`, and namespaced `metadata`
frontmatter, plus the group definitions in `skills.sh.groups.yaml`. It updates:

- `.claude-plugin/marketplace.json` for Claude Code
- `skills.sh.json` for the repository page on skills.sh

It does not generate per-skill plugin manifests. When adding a skill:

1. Add its marketplace metadata to `SKILL.md`.
2. Set `imankulov.skills-sh-group` to an existing title from
   `skills.sh.groups.yaml`, or omit it to leave the skill ungrouped.
3. Edit `skills.sh.groups.yaml` only when adding, renaming, reordering, or describing
   a group.
4. Run the generator.

Check generated metadata without changing files:

```bash
uv run scripts/generate_marketplace.py --check
```

The repository's pre-commit hook runs the generator automatically.

## Cross-Agent Compatibility

This repo uses `AGENTS.md` (read by Cursor, Copilot, Codex, and other AI agents) as
the canonical contributor guide. `CLAUDE.md` redirects here for Claude Code
compatibility.

Skills themselves work across agents via the [Agent Skills specification](https://agentskills.io/specification).
The `SKILL.md` format is agent-agnostic.
