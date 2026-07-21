---
name: editor-pipeline
description: |
  Run a full editorial pass on prose: a content edit (substance, structure, engagement)
  applied directly, then a copy edit (grammar, style, phrasing). Use when the user wants
  the whole edit in one step on an article, blog post, doc, README, or any prose. Also
  use when they say "full edit", "edit pass", "content and copy edit", "polish this end
  to end", or "run it through the editor".
  Do NOT use for: a report-only review with no changes (use editor-content), a
  grammar-only pass (use editor-copy), or agent instruction files (AGENTS.md, SKILL.md,
  CLAUDE.md).
metadata:
  imankulov.skills-sh-group: Writing
  imankulov.skills-sh-order: "25"
  imankulov.claude-display-name: Editor Pipeline
  imankulov.claude-category: development
  imankulov.claude-keywords: "editor,pipeline,agent-skills"
---

# Editor: full pipeline

Run two editing passes on the same file, in order. The editing criteria live in the
other two skills; this one just chains them.

The file(s) to edit: $ARGUMENTS

If no file is given and it is not obvious from context, ask which one before starting.

1. Invoke `editor-content` in apply mode (pass the file plus "apply") — it fixes
   substance and structure in-place.
2. Invoke `editor-copy` on the same file — it fixes grammar, style, and phrasing.

Let the first pass finish before the second, so the copy edit runs on the restructured
text. Then give one combined summary, keeping each skill's own reporting.

Both skills scope their work to the uncommitted diff when the file is tracked in git
(they treat the committed version as already clean). That carries through here: if
editor-content decides the changes are too minor to need a content pass, skip straight
to the copy pass. If the user asks for a full pass, pass that instruction to both
skills.
