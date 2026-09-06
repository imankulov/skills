---
name: connected-chrome
description: |
  Route browser work to the agent's user-facing Chrome integration. Use when the
  task requires an existing Chrome profile, its signed-in state, installed
  extensions, open tabs, or user observation/control. Also use for requests such
  as "use my Chrome," "open this in my profile," or "test the installed extension."
  Do NOT use for ordinary web browsing where the user's actual Chrome state does
  not matter.
metadata:
  imankulov.skills-sh-group: Tools
  imankulov.skills-sh-order: "30"
  imankulov.claude-display-name: Connected Chrome
  imankulov.claude-category: development
  imankulov.claude-keywords: "chrome,browser,profile,extension"
---

# Connected Chrome

Use the current agent's user-facing Chrome integration.

- **Claude Code:** use Chrome MCP.
- **Codex:** use the Chrome integration.
- **Other agents:** use their connected Chrome or external-browser capability.

Use the requested Chrome profile when the user names one. Keep the browser visible
when the user asks to observe or take control.
