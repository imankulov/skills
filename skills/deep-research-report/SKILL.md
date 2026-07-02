---
name: deep-research-report
description: |
  Run a multi-question investigation and produce a durable, multi-page research report
  that lives next to the project: clarify scope, gather evidence with parallel
  sub-agents and real data, build a zensical site with charts and raw data, then
  adversarially review and polish it. Use when the user asks for a deep exploration,
  an improvement review, a technology evaluation, or any research where the answer is
  a report rather than a code change ("explore X and suggest improvements", "research
  whether we should Y", "build a report on Z").
  Do NOT use for: single-fact lookups, quick comparisons that fit in a chat reply, or
  reports the user wants as one throwaway markdown file.
metadata:
  imankulov.skills-sh-group: Research
  imankulov.skills-sh-order: "40"
  imankulov.claude-display-name: Deep Research Report
  imankulov.claude-category: development
  imankulov.claude-keywords: "research,report,investigation,zensical,agent-skills"
---

# Deep research report

Turn a question (or list of questions) into a multi-page report the team keeps. The
report is a living artifact: committed next to the project, structured for follow-up,
and honest about its own methodology.

## 1. Clarify before researching

Explore the environment first (project structure, prior docs on the topic, available
data sources), so your questions are informed rather than generic. Then interview the
user before researching:

- Ask specific questions grounded in what you just explored, with concrete options
  and a recommended default, not open-ended prompts.
- Pin down vague goals ("improve", "better", "worth it") until they name a measurable
  outcome or an explicit trade-off the user accepts.
- One batched round; follow up only when an answer opens a real fork in the research.
  "Use your judgment" is an acceptable answer — note it and move on rather than
  pressing.

Always settle:

- Scope and priorities: which sub-questions deserve depth, which a paragraph.
- Budget for live experiments: may you spend API tokens, run against real data, and
  roughly how freely?
- Where the report lives (follow the repo's existing conventions for research
  artifacts).

Proactively list the access you expect to need and confirm it works before starting:
a production database copy, MCP servers, authenticated CLIs (Sentry, Linear, cloud
providers), API keys for experiments, the team knowledge base. Ask for what's missing
now, not mid-research.

## 2. Research

Fan out. Run independent questions as parallel background sub-agents: web research
(with instructions to verify claims against official/primary pages and flag what they
couldn't verify), codebase exploration, and data analysis each get their own agent.
Keep synthesis and judgment in the main loop. In claude.ai, the built-in
[Research tool](https://support.claude.com/en/articles/11088861-use-research-on-claude)
covers the web-research fan-out.

Ground claims in the strongest evidence available:

- Prefer measured numbers over estimates, and label which is which (e.g. billed API
  cost with caching vs list-price arithmetic — they can invert a ranking).
- Run experiments through the real code paths on real data where permitted.
- Experiment outputs that live in ephemeral stores (a database copy that gets
  re-synced, a trace service with short retention) must be exported to durable files
  the moment they matter.

## 3. Build the report as a site

Use [zensical](https://zensical.org) (`uvx zensical serve|build`, TOML config,
`docs/*.md` pages). Layout:

```
<report-dir>/
├── README.md          # what this is + how to serve/build
├── zensical.toml      # site_name, nav; offline plugin on
├── .gitignore         # site/ and .zensical/
├── docs/
│   ├── index.md       # TLDR: numbered findings + suggested sequencing table
│   ├── <theme>.md     # one page per research theme
│   ├── context.md     # investigation trail (see §6)
│   └── assets/        # charts (SVG) + raw data (JSON/CSV)
└── scripts/           # reproduction artifacts: harnesses, chart generators, notes
```

Writing the pages:

- Every recommendation names its evidence; every number says where it came from.
- When reviewers or sources genuinely disagree and both views hold, keep both: state
  your position in the text and give the dissent an `!!! note "Alternative view"`
  admonition. Don't silently discard either.
- State methodology limits where the reader needs them (sample size, who rated what,
  what the data can't show), not in a disclaimers appendix.

## 4. Charts

Follow the dataviz skill if available (form selection, palette validation, mark
specs). Regardless:

- Pre-rendered SVG images in `docs/assets/` are the most reliable option for a
  zensical site (offline, no plugin system yet); inline Chart.js via raw HTML works
  but needs a vendored JS file.
- Start from this skill's `scripts/charts.py` (validated palette + grouped bars,
  horizontal bars, and labeled scatter): copy it into the report's `scripts/`, adapt
  the `__main__` block to the real data, and commit it so charts are reproducible.
- Render every chart to a bitmap and look at it before shipping — label collisions
  and scale bugs only show up visually. Use whatever the platform offers: `qlmanage
  -t` (macOS), `rsvg-convert` / ImageMagick, or a headless-browser screenshot.

## 5. Adversarial review, then polish

Spawn a critical-review sub-agent that has access to the same evidence sources you
used (database, codebase, web) and instruct it to re-verify facts independently and
to push back on your recommendations, not just proofread. Expect it to find real
errors; this pass earns its cost.

- Factual errors: fix.
- Clear gaps (a risk unaddressed, an inconsistency between pages): fix.
- Judgment disagreements where both positions survive scrutiny: add as alternative
  view, keep yours.

If the review challenges your methodology (it should), answer in the report itself —
a "how representative is this?" section beats a rebuttal in chat.

Then run /editor-pipeline over all pages. Guard against meaning drift: snapshot the
docs first and diff afterwards; verify no numbers changed.

## 6. Required artifacts

**`docs/context.md`** — the investigation trail, written for the next agent (or
future you) who continues this work. Include: every question that drove the research
(initial and follow-ups, in order, with one-line outcomes); dead ends and traps that
cost time; context explored but not used in the report; external links actually
consulted (flag any load-bearing claim left unverified); the exact commands used to
query data, run experiments, and generate charts; and open threads for follow-up
tasks. The report pages carry conclusions; this page carries the trail.

**Raw data** — if the research generated data (benchmark runs, survey of records,
scraped tables), commit the raw records to `docs/assets/` and the scripts that
produced them to `scripts/`. Include subjective assessments (ratings, per-item notes)
so the headline numbers are auditable. A report whose central evidence can't be
re-examined is an opinion with charts.

## Done when

- [ ] `zensical build` passes; every page reachable from nav
- [ ] Charts render correctly (visually checked)
- [ ] Adversarial review ran; findings fixed or captured as alternative views
- [ ] /editor-pipeline ran; numbers verified unchanged
- [ ] context.md and raw data committed
- [ ] User told how to read it (`uvx zensical serve -o`) and what the headline
      findings are
