---
name: docstore
description: |
  Document-collection data organization for semi-structured repositories. MUST be
  consulted whenever creating, moving, or organizing files in a repository that declares
  docstore conventions in its agent instructions file (CLAUDE.md, AGENTS.md, or similar).
  Also use when the user asks where to put a file,
  how to structure content, creates meeting notes, adds a new entity (client, provider,
  article, topic), or organizes any non-code documents. Triggers on any file creation or
  modification in repos with collection-based directory structure, even if the user does
  not mention "docstore" explicitly.
  Do NOT use for: code-only repositories, package/module organization, or CI/CD config.
---

# Docstore: Document-Collection Data Organization

Organize semi-structured documents using a pattern inspired by document databases
(collections → documents → fields). Repositories declare their schema in the project's
agent instructions file (CLAUDE.md, AGENTS.md, or similar — referred to as "the
instructions file" below). Always read it first to understand the project's specific
structure.

## Core model

### Recursive type/instance pairs

Every directory is either a **type** (collection) or an **instance** (document). They
strictly alternate:

```
type/instance/type/instance/...
```

- **Type directories** (collections) group documents of the same kind.
- **Instance directories** (documents) contain files about one specific entity.
- **Files** (fields) live only at instance levels.

The pattern is recursive — documents can contain nested collections. However, **flat is
better than nested**. One level of nesting (type/instance) handles most cases. Two levels
(type/instance/type/instance) are acceptable when the data naturally calls for it — e.g.,
a client has multiple meetings. Nesting beyond two levels should be rare and justified by
the structure of the data, not by a desire to categorize.

```
clients/                            # type (level 1)
  acme-corp/                        # instance (level 1)
    README.md                       # field (primary)
    meetings/                       # type (level 2) — OK, a client has many meetings
      2026-01-15/                   # instance (level 2)
        README.md                   # field
        summary.md                  # field
```

When tempted to add a third level, consider whether files in the parent document
directory would suffice instead.

### Singletons

Documents that don't belong to any collection live at the repo root. They have
project-level importance and must be listed in the instructions file under a "Singletons"
section. The instructions file itself is the top-level singleton.

Examples: a glossary, a cross-cutting comparative report, a project roadmap.

### README.md is the spine

Every instance directory MUST have a `README.md`. It serves three roles:

1. **Primary document** — the main content about this entity.
2. **File index** — lists sibling files with one-line descriptions.
3. **Nested collection index** — lists sub-collections when they exist.

If a document has only one thing to say, that goes in README.md and no other files are
needed.

When adding files to a document directory, always update its README.md to reference them.

**Example** — a minimal meeting README:

```markdown
# Meeting with Jane Smith — 2026-01-15

Quarterly review. ~30 min.

## Files

- [summary.md](summary.md) — Key decisions and action items
- [transcript.md](transcript.md) — Raw meeting transcript
```

## Naming conventions

| What | Convention | Examples |
|---|---|---|
| Type (collection) | kebab-case, plural | `clients`, `meetings`, `knowledge-base` |
| Instance (document) | kebab-case, by entity or date | `acme-corp`, `2026-01-15` |
| Files (fields) | snake_case.ext | `summary.md`, `action_items.md` |
| Primary file | Always `README.md` | — |
| Default format | Markdown (`.md`) | `.json` for structured data |

## File policies

- **Binary sources** (received PDFs, signed contracts, scanned docs): commit in the
  document directory.
- **Binary derivatives** (`.docx` exported from `.md`, generated PDFs): ephemeral — do
  not commit.
- **Cross-references**: relative markdown links —
  `[Acme Corp](../../clients/acme-corp/README.md)`.

## The instructions file as schema registry

The project's agent instructions file (CLAUDE.md, AGENTS.md, or equivalent) declares the
repo's data schema:

1. **Collections** — top-level type directories with one-line descriptions.
2. **Singletons** — root-level files with one-line descriptions.
3. **Patterns** — recurring file conventions across documents (e.g., what `summary.md`
   always contains in a meetings collection).

When creating a new top-level collection or singleton, update the instructions file.

**Example** schema section (in CLAUDE.md, AGENTS.md, etc.):

```markdown
## Data organization

This repository uses docstore conventions. Consult the `docstore` skill when creating
or modifying files.

Collections:
- `clients/` — Customer accounts, contacts, and interaction history
- `knowledge-base/` — Support articles grouped by product area
- `templates/` — Reusable document templates

Singletons:
- `quarterly-report.md` — Cross-client quarterly summary
- `glossary.md` — Internal terminology reference

Patterns:
- `*/*/meetings/<date>/summary.md` — Structured meeting summary with action items
- `*/*/meetings/<date>/transcript.md` — Raw meeting transcript
- `knowledge-base/*/common-issues/*/README.md` — Known issue with symptoms and resolution
```

## Decision guide

### Collection vs singleton

- Multiple instances of the same kind → **collection** (`clients/`, `knowledge-base/`).
- One-of-a-kind, cross-cutting, project-level → **singleton** (`glossary.md`).
- Unsure → start as singleton, promote to collection when a second instance appears.

### When to nest

- Sub-items are distinct instances of a type (multiple meetings, multiple contracts) →
  **nest**: create a type/instance sub-directory (`meetings/2026-01-15/`).
- Multiple files describe the same thing (summary + transcript of one meeting) →
  **keep flat**: files in the same instance directory.

### Workflow for creating new content

1. Read the instructions file to understand the existing schema.
2. Identify where the content belongs (existing collection? new collection? singleton?).
3. Create the instance directory with README.md as the first file.
4. Add additional field files as needed.
5. Update the parent document's README.md to reference the new content.
6. If a new top-level collection or singleton was created, update the instructions file.

## Verification

- [ ] Every instance directory has a README.md
- [ ] README.md references all sibling files and nested collections
- [ ] New top-level collections and singletons are listed in the instructions file
- [ ] No binary derivatives committed (only binary sources)
- [ ] Cross-references use relative markdown links
- [ ] Directory names follow type=plural/instance=entity convention
