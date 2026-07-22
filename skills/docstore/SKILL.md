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
metadata:
  imankulov.skills-sh-group: Tools
  imankulov.skills-sh-order: "10"
  imankulov.claude-display-name: Docstore
  imankulov.claude-category: development
  imankulov.claude-keywords: "docstore,agent-skills"
---

# Docstore: Document-Collection Data Organization

Organize semi-structured documents using a pattern inspired by document databases
(collections → documents → fields). Repositories declare their schema in the project's
agent instructions file (CLAUDE.md, AGENTS.md, or similar — "the instructions file"
below). Read it first to understand the project's specific structure.

## Core model

### Recursive type/instance pairs

Every directory is either a **type** (collection) or an **instance** (document), strictly
alternating: `type/instance/type/instance/...`

- **Type directories** (collections) group documents of the same kind.
- **Instance directories** (documents) contain files about one specific entity.
- **Files** (fields) live only at instance levels.

Prefer flat over nested. One level (type/instance) handles most cases. Nest a second
level only when an instance naturally contains its own collection — e.g., a client with
multiple meetings. Beyond two levels should be rare, justified by the data's structure and not a
desire to categorize; before nesting, check whether files in the parent document
directory would suffice.

```
clients/                # type (level 1)
  acme-corp/            # instance (level 1)
    README.md           # field (primary)
    meetings/           # type (level 2) — a client has many meetings
      2026-01-15/       # instance (level 2)
        README.md       # field
        summary.md      # field
```

Keep multiple files that describe one entity as sibling fields in its instance directory:
the summary and transcript of a single meeting stay together, not split into
sub-directories.

### Singletons

Documents that belong to no collection live at the repo root — one-of-a-kind,
cross-cutting, project-level items such as a glossary, a comparative report, or a
roadmap. List each in the instructions file under a "Singletons" section. The
instructions file itself is the top-level singleton.

### README.md is the spine

Every instance directory MUST have a `README.md`, serving three roles:

1. **Primary document** — the main content about this entity.
2. **File index** — lists sibling files with one-line descriptions.
3. **Nested collection index** — lists sub-collections when they exist.

If a document has only one thing to say, it goes in README.md and no other files are
needed. Whenever you add files to a document directory, update its README.md to reference
them.

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

The instructions file declares the repo's data schema in three parts:

1. **Collections** — top-level type directories with one-line descriptions.
2. **Singletons** — root-level files with one-line descriptions.
3. **Patterns** — recurring file conventions across documents, written as path globs
   (e.g., `*/*/meetings/<date>/summary.md` — structured meeting summary with action
   items).

Update the instructions file whenever you create a new top-level collection or singleton.

## Collection vs singleton

Multiple instances of the same kind → collection; one-of-a-kind and cross-cutting →
singleton. Unsure → start as a singleton and promote to a collection when a second
instance appears.
