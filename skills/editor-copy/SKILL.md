---
name: editor-copy
description: |
  Copy-edit written content: fix grammar, style, and phrasing errors directly in the
  file. Use when the user asks to proofread, copy-edit, or clean up an article, blog
  post, doc, README, email, or any prose. Also use when they say "fix the grammar",
  "tighten this up", or "do a copy pass".
  Do NOT use for: structural or engagement review (use the editor-content skill), or
  agent instruction files (AGENTS.md, SKILL.md, CLAUDE.md).
metadata:
  imankulov.skills-sh-group: Writing
  imankulov.skills-sh-order: "40"
  imankulov.claude-display-name: Editor Copy
  imankulov.claude-category: development
  imankulov.claude-keywords: "editor,copy,agent-skills"
---

# Editor: copy edit

Copy-edit the file as an expert editor.

The file(s) to copy-edit: $ARGUMENTS

If no file is given, or not immediately obvious from previous discussion or context, ask which file or text to edit.

## Scope: what to edit

If the file is tracked in git, assume the committed version (HEAD) is already clean.
Run `git diff HEAD -- <file>` and copy-edit only the changed hunks, reading just
enough surrounding lines to understand tone and to make Edit matches unique. Do not
re-edit unchanged text.

Do a full pass instead when any of these hold:

- the file is untracked or not in a git repository;
- the diff against HEAD is empty (the user invoked the skill on a committed file, so
  they want the whole thing checked);
- the user asks for a full pass or says the committed version was never edited.

If the file (or the relevant hunks) is already in context and unchanged since, work
from context instead of re-reading.

## Process

1. Invoke the `writing` skill via the Skill tool to load the prose guidelines.
2. Determine the scope (changed hunks or full file) and read what it requires.
3. Edit each issue in-place with the Edit tool.
4. After all edits, give a brief summary of the changes.

## Constraints

- Fix glaring grammar and style errors, not stylistic preferences.
- Prefer phrasings closest to the original.
- Limit edits to grammar and phrasing, without rewriting content, adding information, or touching code blocks.
- Flag unclear meaning as a question rather than guessing.
- If the writing is already good, say so.
