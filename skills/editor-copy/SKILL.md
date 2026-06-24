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

Copy-edit the file as an expert editor. Apply the writing skill's guidelines.

The file(s) to copy-edit: $ARGUMENTS

If no file is given, or not immediately obvious from previous discussion or context, ask which file or text to edit.

## Process

1. Invoke the `writing` skill via the Skill tool to load the prose guidelines.
2. Read the entire file to understand context and tone.
3. Edit each issue in-place with the Edit tool.
4. After all edits, give a brief summary of the changes.

## Constraints

- Fix glaring grammar and style errors, not stylistic preferences.
- Prefer phrasings closest to the original.
- Do not rewrite content, add information, or touch code blocks.
- Flag unclear meaning as a question rather than guessing.
- If the writing is already good, say so.
