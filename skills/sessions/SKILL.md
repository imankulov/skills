---
name: sessions
description: |
  List past Claude Code sessions for the current project. Use when the user asks
  to see their session history, find a previous conversation, list past sessions,
  or look up what they worked on before. Also use when they say "show me my sessions",
  "what did I work on last week", or "find the session where I...".
  Do NOT use for: resuming sessions (use `claude --resume`), or managing session
  settings.
metadata:
  imankulov.skills-sh-group: Tools
  imankulov.skills-sh-order: "30"
  imankulov.claude-display-name: Sessions
  imankulov.claude-category: development
  imankulov.claude-keywords: "sessions,agent-skills"
---

# Sessions

List and browse past Claude Code sessions for the current project.

## Usage

Run the helper script to list sessions:

```bash
python <skill-path>/scripts/list_sessions.py [project-dir] [--all] [--json]
```

- Default: shows the 20 most recent sessions for the current working directory
- `--all`: show every session, not just the last 20
- `--json`: output as JSON instead of a markdown table

Present the script's output verbatim — don't summarize the table or drop rows, and
keep session IDs as full UUIDs, since truncated IDs don't work with `--resume`.

After the table, remind them how to resume:

- From the terminal: `claude --resume <session-id>`
- Inside an active session: `/resume` opens an interactive picker (search with `/` or
  any character to filter); `/resume <name>` resumes a named session directly
- To fork (branch) a session without modifying the original:
  - From the terminal: `claude --resume <session-id> --fork-session`
  - Inside an active session: `/branch` copies the conversation into a new session ID

## Interpreting results

- **Turns** — `5u/8a` means 5 user messages, 8 assistant messages
- **Size** — JSONL file size; larger sessions had more tool use and context
