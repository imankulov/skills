---
name: editor-content
description: |
  Review written content for engagement and clarity from a reader's perspective.
  Use when the user asks to review a draft, find weak spots, check whether content
  holds attention, or get a content edit on an article, blog post, doc, README,
  proposal, or any prose. Also use when they say "review this", "where does this
  drag", "is this engaging", or "do a content pass". By default it only reports
  issues in a table; if the user asks to fix, apply, address, or auto-improve, it
  edits the file directly and reports what changed.
  Do NOT use for: grammar, spelling, and phrasing fixes (use the editor-copy skill),
  or agent instruction files (AGENTS.md, SKILL.md, CLAUDE.md).
metadata:
  imankulov.skills-sh-group: Writing
  imankulov.skills-sh-order: "30"
  imankulov.claude-display-name: Editor Content
  imankulov.claude-category: development
  imankulov.claude-keywords: "editor,content,agent-skills"
---

# Editor: content review

Review the content as a reader, not a copy editor. Your job is to find where the text
stops being interesting or becomes confusing, not to fix grammar.

Arguments: $ARGUMENTS

The arguments may name the file(s) to review and/or specify the mode (e.g. "review
and fix x.md", "apply"). If no file is given, or not immediately obvious from previous
discussion or context, ask which file or text to review.

## Scope: when a content pass is needed

If the file is tracked in git, assume the committed version (HEAD) is already clean.
Run `git diff HEAD -- <file>` first:

- **Diff is empty, file untracked, or the user asks for a full review** — review the
  whole file as described below.
- **Changes are minor** (typo fixes, small phrasing tweaks, a few lines that don't
  affect structure, flow, or the document's argument) — say that the changes are too
  minor to need a content pass and stop. Don't review the rest of the file.
- **Changes are substantial** (new or rewritten sections, reordered structure, changed
  claims) — read the whole file for context, since structure and flow can't be judged
  from a diff, but focus your findings on the changed sections and the parts they
  affect (transitions into and out of them, the title, the summary). Don't re-litigate
  untouched sections the committed version already got right.

If the file is already in context and unchanged since, work from context instead of
re-reading it.

## What to look for

- **Engagement drops** — sections that feel flat, repetitive, or drag.
- **Unclear meaning** — sentences a reader would need to re-read.
- **Structure problems** — jumps in logic, missing context, a buried lead.
- **Tone mismatch** — too formal, too generic, or off from the author's established voice.
- **Triplets** — three-item lists or parallel clauses (X, Y, and Z) that feel formulaic.
  One or two items usually suffice. Flag every instance except ones that describe an
  actual structure (e.g. listing three real building blocks).
- **Overexplaining** — sentences that spell out what the reader already knows from a
  preceding sentence, an example, code, or basic context.
- **Overselling setups** — "The trick that makes it work:", "Here's where it gets
  interesting:", "The key insight is:" and similar reveal-setups that promise a clever
  point before delivering it. These are AI tells. Just state the fact.
- **Setup-subvert-reveal** — "I expected X. It wasn't. Y." where a short dramatic
  negation creates artificial suspense before the real point. Collapse into one
  sentence: "X turned out to be Y."
- **AI-tell sentence patterns** — comma-separated negative lists used as emphasis
  ("No X, no Y, no Z"), predicate-less closers ("Same result, achieved with a flag"),
  dramatic contrast pairs where a short limitation sentence sets up a short payoff
  sentence ("X only does A. Y supports 30+ B's."), and "What X is" cleft openers
  ("What I like most is...").
- **Title** — too long, too vague, or buries the point.
- **Metadata** — if the document has a summary, description, or front matter, does it
  accurately represent the content?
- **Visual rhythm** — long stretches of unbroken prose that would benefit from a code
  block, figure, callout, blockquote, table, or list. Only suggest elements that carry
  information, not decoration.

Do not flag grammar or phrasing issues — that is the editor-copy skill's job.

## Modes

Default to Review. Switch to Apply only when the user asks up front to apply, fix,
address, or auto-improve the content (e.g. "review and fix", "address all of them",
"auto-improve this").

## Output format

### Review mode

Return a markdown table and do NOT edit the file. The author decides what to act on.

| #   | Location         | Issue                                      | Suggestion               |
| --- | ---------------- | ------------------------------------------ | ------------------------ |
| 1   | Section or quote | What's wrong from the reader's perspective | How it could work better |

### Apply mode

Find every issue, then fix each one in-place with the Edit tool. Address them all,
not just the easy ones. Keep edits faithful to the author's voice and meaning; when a
fix would change the substance or you're unsure of intent, leave the text alone and
note it as skipped rather than guessing.

After editing, report what you did in the same table, with a final column for the
outcome:

| #   | Location         | Issue                  | Change made                          | Status   |
| --- | ---------------- | ---------------------- | ------------------------------------ | -------- |
| 1   | Section or quote | What was wrong         | What you changed it to               | Applied  |
| 2   | Section or quote | What was wrong         | Why you left it                      | Skipped  |

In both modes, if the content reads well and holds attention throughout, say so.
