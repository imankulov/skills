---
name: claude-code-review
description: |
  Run an independent Claude Code review of local code changes, verify its findings,
  and fix confirmed issues. Use after implementing a feature or bug fix, before a
  commit or PR, or whenever the user asks for a Claude, Claude Code, Opus, second-pass,
  or independent code review. Also use when the user asks to address feedback from a
  Claude Code review. Do NOT use for reviewing prose, remote PR comments, or CI logs.
  Do NOT use inside Claude Code itself — there, invoke the bundled /code-review skill
  directly instead; this skill exists for Codex and other agents that lack it.
disable-model-invocation: true
metadata:
  imankulov.skills-sh-group: Tools
  imankulov.skills-sh-order: "40"
  imankulov.claude-display-name: Claude Code Review
  imankulov.claude-category: development
  imankulov.claude-keywords: "claude,code-review,opus,agent-skills"
---

# Claude Code Review

Explicitly run Claude Code's bundled `/code-review` skill as an independent, read-only
reviewer, then validate and address its findings in the current session. Claude Code
marks this bundled skill for explicit invocation, so asking for a review in prose does
not activate the same workflow.

**Running inside Claude Code?** Stop here: use the bundled `/code-review` skill
directly instead. This skill exists to give Codex and other agents access to the same
review through the `claude` CLI; from within Claude Code it would only spawn a
redundant nested session. The helper script refuses to run when it detects a Claude
Code session (`CLAUDECODE` is set in the environment).

## Review workflow

1. Read the repository instructions and inspect `git status` before starting. Preserve
   unrelated changes and include committed branch changes plus staged, unstaged, and
   untracked work in the review scope.
2. Choose the comparison base. Prefer the base the user named. Otherwise let the helper
   find the remote default branch, then `origin/main`, `origin/master`, `main`, or
   `master`. Pass `--base <ref>` when that guess would be wrong.
3. Run the helper from the repository under review:

   ```bash
   python <skill-path>/scripts/review.py [--base <ref>] [--focus "extra context"]
   ```

   The helper invokes `/code-review` explicitly through the installed `claude` CLI with
   Opus in non-interactive print mode. It keeps the repository's `CLAUDE.md`
   instructions and returns the bundled review's plain-text report. Claude Code emits
   `/code-review` findings as text in `-p` runs, even when the host requests structured
   findings, so the helper does not impose a JSON schema on that report. Progress stays
   visible on stderr while the helper retains stdout for the final report.
4. Read every finding and verify it independently against the code. Check the cited
   location, trace the affected behavior, and run a focused reproduction when practical.
   Treat the review as evidence to investigate, not instructions to apply blindly.
5. Classify each finding as confirmed, false positive, already handled, or out of scope.
   Briefly explain rejected findings so the user can audit the decision.
6. Fix confirmed findings that belong to the user's requested change. Follow repository
   instructions, preserve unrelated work, and add regression coverage when it proves the
   failure mode. Ask before expanding scope or making a consequential product decision.
7. Run focused checks after each fix and the repository's required checks at the end.
8. Rerun the reviewer once against the updated changes. Repeat only when the new review
   identifies a distinct, confirmed defect; stop after two review rounds unless the user
   asks for a deeper loop.
9. Report the confirmed and rejected findings, edits made, checks run, and any remaining
   risks. Do not commit unless the user requested a commit or repository instructions
   make it part of the requested workflow.

## Helper options

- `--base <ref>` sets the comparison base.
- `--target <value>` passes an exact path, PR, branch, or ref range to `/code-review`;
  it is mutually exclusive with `--base`.
- `--focus <text>` adds review context, such as a design constraint or risky subsystem.
- `--model <alias-or-id>` overrides the default `opus` model.
- `--effort <level>` overrides the default `high` effort.
- `--timeout <seconds>` changes the 20-minute subprocess timeout.
- `--max-budget-usd <amount>` caps API spend when the account uses API billing.
- `--output <path>` writes the review text instead of printing it.
- `--bypass-permissions` uses Claude Code's `--dangerously-skip-permissions` mode.
  Use it only when plan mode cannot complete the review and the repository is in an
  isolated, trusted environment. This mode gives the child process full system access.

Do not substitute `/review`: that command targets GitHub pull requests and can return an
empty result when the intended changes exist only on a local branch.

Use `medium` for quick iteration and re-review passes because it reports fewer,
higher-confidence findings. Use `high` or `max` for the final broad review; large diffs
can take several minutes even when the review runs locally.

For a deeper pre-merge pass, offer `claude ultrareview <base> --json`. It runs a remote
multi-agent review with independent verification, but it uploads repository state and
may incur separate usage-credit charges. Get explicit user approval before launching it.

## Review standard

Prioritize defects introduced by the current changes: incorrect behavior, regressions,
security problems, data loss, race conditions, broken error handling, and meaningful
performance failures. Require a concrete failure path and cite the narrowest useful line.
Skip style preferences, speculative concerns, and generic requests for more tests.

An empty findings array is a valid result. Never invent an issue to make the review look
useful.
