---
name: screenshot-maker
description: Create beautiful, documentation-ready screenshots of web pages or specific page sections. Use when the user wants to capture a screenshot for docs, READMEs, blog posts, or marketing — especially when they mention framing, shadows, rounded corners, blurring sensitive info, or targeting a specific element/section. Also use when the user says "take a screenshot of", "capture this section", "screenshot for the docs", or wants polished visuals of a web UI.
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*), Bash(magick:*), Bash(magick), Bash(python:*)
metadata:
  imankulov.skills-sh-group: Tools
  imankulov.skills-sh-order: "20"
  imankulov.claude-display-name: Screenshot Maker
  imankulov.claude-category: development
  imankulov.claude-keywords: "screenshot,maker,agent-skills"
---

# Screenshot Maker

Create polished, documentation-ready screenshots of web pages or page sections with professional framing (rounded corners, shadows, gradient backgrounds) and optional blurring and highlighting.

## Prerequisites

- **agent-browser** — browser automation CLI (`brew install agent-browser` or `npm i -g agent-browser`)
- **ImageMagick 7** — image processing (`brew install imagemagick`)

## Gathering requirements

When the user's request is ambiguous (e.g. "take a screenshot of this page"), use AskUserQuestion to clarify before doing work. Ask up to two questions in one call — pick only the ones that aren't already clear from context.

**Question 1 — Target element.** Having an exact CSS selector makes everything faster and more reliable. If the user hasn't provided one, ask:

```
question: "Which part of the page should I capture? If you can provide a CSS selector (right-click → Inspect → Copy selector), that speeds things up a lot."
options:
  - "Full visible page"
  - "A specific section (I'll describe it)"
  - "I have a CSS selector"
```

**Question 2 — Styling.** If the user hasn't specified framing preferences:

```
question: "How should the screenshot look?"
options:
  - "Framed (rounded corners, shadow, gradient background)" — the default professional look
  - "Raw capture, no framing"
  - "I have specific preferences (colors, highlight, blur, etc.)"
```

## Core workflow

### 1. Navigate and set viewport

```bash
agent-browser open <url> && agent-browser wait --load networkidle
agent-browser set viewport 1280 900
```

### 2. Prepare the page and capture

The `scripts/prepare.py` script handles all browser-side preparation. It shells out to `agent-browser` under the hood.

**Capture an element** (with automatic viewport-crop fallback when element screenshots render blank):

```bash
python <skill-path>/scripts/prepare.py crop --selector "section.hero" --output /tmp/raw.png
```

**Hide page chrome** (navbars, footers, cookie banners — anything fixed/sticky):

```bash
python <skill-path>/scripts/prepare.py hide-chrome
```

**Hide specific elements:**

```bash
python <skill-path>/scripts/prepare.py hide --selector "nav, .sidebar, .cookie-banner"
```

**Finding the right selector.** When the user describes what they want by name ("the Pricing section", "the feature cards"), use `agent-browser snapshot -i` or `agent-browser snapshot -s "<selector>"` to discover the page structure, then pass the container's CSS selector to `prepare.py crop`.

### 3. Blur sensitive information

**Blur elements by CSS selector:**

```bash
python <skill-path>/scripts/prepare.py blur --selector ".api-key, .secret-value"
```

**Blur specific text anywhere on the page:**

```bash
python <skill-path>/scripts/prepare.py blur --text "sk-proj-abc123"
```

**Adjust blur radius** (default 5px — `4` is subtle, `8` is heavy):

```bash
python <skill-path>/scripts/prepare.py blur --text "password123" --radius 8
```

### 4. Highlight elements

Draw attention to a specific element. Two modes:

**Border mode** (default) — colored rounded outline around the element:

```bash
python <skill-path>/scripts/prepare.py highlight --selector "#feature-card" --mode border
python <skill-path>/scripts/prepare.py highlight --selector ".cta" --mode border --color "#3b82f6" --thickness 2
```

**Spotlight mode** — dims the entire page except the target element:

```bash
python <skill-path>/scripts/prepare.py highlight --selector "#feature-card" --mode spotlight
python <skill-path>/scripts/prepare.py highlight --selector ".hero" --mode spotlight --opacity 0.6
```

Options:
- `--mode border|spotlight` — highlight style (default: border)
- `--padding <px>` — space between element and highlight edge (default: 6)
- `--border-radius <px>` — corner radius of the highlight (default: 4)
- `--color <color>` — border color, border mode only (default: #ef4444)
- `--thickness <px>` — border width, border mode only (default: 3)
- `--opacity <0-1>` — dim overlay darkness, spotlight mode only (default: 0.5)

Run the hide, blur, and highlight commands before `crop` — they modify the live page, and `crop` takes the screenshot.

### 5. Frame with ImageMagick

Apply professional framing to the raw screenshot:

```bash
python <skill-path>/scripts/frame.py /tmp/raw.png /tmp/final.png [options]
```

Options:
- `--padding <px>` — inner padding around content (default: 20)
- `--radius <px>` — corner radius for the content card (default: 4)
- `--shadow-blur <px>` — shadow softness (default: 15)
- `--shadow-opacity <pct>` — shadow darkness 0-100 (default: 30)
- `--bg-start <color>` — gradient start color (default: #2c3e50)
- `--bg-end <color>` — gradient end color (default: #4ca1af)
- `--bg-margin <px>` — space between card edge and background edge (default: 40)
- `--resize <WxH>` — resize final image (e.g. `800x`), maintains aspect ratio
- `--no-bg` — skip the gradient background, output card with shadow on transparent
- `--trim` — auto-trim whitespace from the raw screenshot before framing

Pipeline: trim (optional) → pad → round corners → drop shadow → gradient background → optional resize.

### Background presets

Instead of `--bg-start` / `--bg-end`, use a preset:

| Preset | Colors | Good for |
|--------|--------|----------|
| `--preset slate` | #2c3e50 → #4ca1af | Professional, subdued **(default)** |
| `--preset ocean` | #667eea → #764ba2 | General purpose |
| `--preset sunset` | #f093fb → #f5576c | Warm, energetic |
| `--preset forest` | #11998e → #38ef7d | Nature, success states |
| `--preset ember` | #ff9a9e → #fecfef | Soft, friendly |
| `--preset midnight` | #0f0c29 → #302b63 | Dark, dramatic |

## Tips

- **Retina screenshots**: `agent-browser set viewport <W> <H> 2` gives 2x resolution at the same CSS layout size.
- **Consistency**: when capturing several screenshots for the same doc page, reuse the same preset and settings.
- **Close browser when done**: `agent-browser close`.
