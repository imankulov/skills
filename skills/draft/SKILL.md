---
name: draft
description: |
  Draft text intended for humans: Slack messages, emails, proposals, summaries,
  architecture docs, product briefs, or any prose the user wants to review and edit
  before sharing. Use when the user asks to draft, compose, or write something — even
  if they don't say "draft" explicitly. Also use when they say things like "put together
  a Slack message", "help me respond to this", "write up a proposal", "summarize what
  we found", or "save this to a draft".
metadata:
  imankulov.skills-sh-group: Writing
  imankulov.skills-sh-order: "20"
  imankulov.claude-display-name: Draft
  imankulov.claude-category: development
  imankulov.claude-keywords: "draft,agent-skills"
---

# Draft

Draft text for humans to read: a Slack reply, an email, an architecture proposal, a
summary of an exploration, a product brief, or anything else the user wants to review
before sharing.

## Workflow

### 1. Load the writing skill

Invoke `/writing` via the Skill tool. Do this before writing anything.

### 2. Determine the format

Ask yourself (don't ask the user unless genuinely ambiguous):

| Context clues | Format |
|---|---|
| "Slack message", "reply in Slack" | **Slack message** — body only, no subject line |
| "email", "draft an email" | **Email** — subject line and body |
| "proposal", "write-up", "summary", "brief" | **Document** — title, sections, markdown formatted |
| No clear context | **Generic** — body only, markdown formatted |

### 3. Write the draft

- Apply the `/writing` skill rules throughout
- Match the user's intent for tone — if they say "hedge it" or "be diplomatic", adjust
  accordingly, but stay clear
- Scale length to the content. A Slack reply might be two sentences; an architecture
  proposal might need sections with headings. Don't pad short things or compress long
  ones — let the subject dictate the length

### 4. Save to a temp file and open in VS Code

Create a markdown file at `/tmp/draft-<descriptive-slug>.md` (e.g.
`draft-auth-redesign-proposal.md`), then open it:

```bash
code /tmp/draft-<descriptive-slug>.md
```

Tell the user the full path so they can find and edit it.

## Conventions

- Open with the substance. Never start with "I hope this message finds you well" or
  "Just wanted to reach out."
- Close only when the message genuinely asks a question. Don't tack on "Let me know if
  you have any questions!" or similar filler sign-offs.
- Use paragraphs by default; reach for bullets only when a list reads better.
