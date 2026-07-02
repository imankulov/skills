"""Static SVG chart generator for research reports.

Copy this file into the report's scripts/ directory and adapt the __main__
block. Design follows the dataviz method: thin marks with rounded data-ends,
hairline grid, muted axis ink, system-ui type, direct value labels, and
<title> elements for native hover tooltips. The palette below is a validated
colorblind-safe default; swap in your brand's values and re-validate if you
have a palette validator available.

Charts: grouped_bars (vertical, multi-series), hbars (horizontal, single
series), scatter (direct-labeled points). All output self-contained SVG that
renders offline and embeds in a zensical page via ![alt](assets/name.svg).
"""

import sys
from pathlib import Path

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/assets")
OUT.mkdir(parents=True, exist_ok=True)

# Palette (dataviz reference, light mode)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASE = "#c3c2b7"
BLUE = "#2a78d6"
AQUA = "#1baf7a"
YELLOW = "#eda100"
VIOLET = "#4a3aa7"
RED = "#e34948"
FONT = 'font-family="system-ui, -apple-system, Segoe UI, sans-serif"'


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def bar_path(x, y, w, h, r=4):
    """Vertical bar with rounded top corners only, anchored to baseline."""
    r = min(r, w / 2, h)
    return (f"M{x},{y + h} L{x},{y + r} Q{x},{y} {x + r},{y} "
            f"L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} L{x + w},{y + h} Z")


def hbar_path(x, y, w, h, r=4):
    """Horizontal bar with rounded right corners only."""
    r = min(r, h / 2, w)
    return (f"M{x},{y} L{x + w - r},{y} Q{x + w},{y} {x + w},{y + r} "
            f"L{x + w},{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} L{x},{y + h} Z")


def nice_ticks(vmax, n=4):
    import math
    raw = vmax / n
    mag = 10 ** math.floor(math.log10(raw))
    for mult in (1, 2, 2.5, 5, 10):
        step = mult * mag
        if vmax / step <= n:
            break
    ticks = []
    v = 0
    while v <= vmax + 1e-9:
        ticks.append(round(v, 6))
        v += step
    if ticks[-1] < vmax:
        ticks.append(round(ticks[-1] + step, 6))
    return ticks


def grouped_bars(filename, title, cats, series, width=760, height=340):
    """series: list of (name, color, values, label_color)."""
    ml, mr, mt, mb = 46, 16, 54, 34
    pw, ph = width - ml - mr, height - mt - mb
    vmax = max(max(vals) for _, _, vals, _ in series)
    ticks = nice_ticks(vmax)
    vmax = ticks[-1]
    n, k = len(cats), len(series)
    slot = pw / n
    bw = min(28, (slot * 0.62 - 2 * (k - 1)) / k)
    group_w = bw * k + 2 * (k - 1)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
         f'<rect width="{width}" height="{height}" fill="{SURFACE}" rx="8"/>',
         f'<text x="{ml}" y="24" {FONT} font-size="15" font-weight="600" fill="{INK}">{esc(title)}</text>']
    # legend
    lx = ml
    for name, color, _, _ in series:
        p.append(f'<circle cx="{lx + 5}" cy="38" r="5" fill="{color}"/>')
        p.append(f'<text x="{lx + 15}" y="42" {FONT} font-size="12" fill="{INK2}">{esc(name)}</text>')
        lx += 15 + 8 * len(name) + 26
    # grid + y labels
    for t in ticks:
        y = mt + ph - (t / vmax) * ph
        if t > 0:
            p.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml + pw}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        p.append(f'<text x="{ml - 8}" y="{y + 4:.1f}" {FONT} font-size="11" fill="{MUTED}" '
                 f'text-anchor="end">{int(t)}</text>')
    p.append(f'<line x1="{ml}" y1="{mt + ph}" x2="{ml + pw}" y2="{mt + ph}" stroke="{BASE}" stroke-width="1"/>')
    # bars
    for i, cat in enumerate(cats):
        gx = ml + i * slot + (slot - group_w) / 2
        for j, (name, color, vals, lcolor) in enumerate(series):
            v = vals[i]
            h = (v / vmax) * ph
            x = gx + j * (bw + 2)
            y = mt + ph - h
            p.append(f'<path d="{bar_path(x, y, bw, h)}" fill="{color}">'
                     f'<title>{esc(cat)} — {esc(name)}: {v}</title></path>')
            p.append(f'<text x="{x + bw / 2:.1f}" y="{y - 5:.1f}" {FONT} font-size="10.5" '
                     f'fill="{lcolor}" text-anchor="middle">{v}</text>')
        p.append(f'<text x="{ml + i * slot + slot / 2:.1f}" y="{mt + ph + 18}" {FONT} font-size="11.5" '
                 f'fill="{INK2}" text-anchor="middle">{esc(cat)}</text>')
    p.append("</svg>")
    (OUT / filename).write_text("\n".join(p))
    print("wrote", filename)


def hbars(filename, title, items, width=760, color=BLUE, unit="", height=None, fmt=None):
    """items: list of (label, value) sorted desc. Single-series horizontal bars."""
    row_h, gap = 26, 8
    ml, mr, mt, mb = 210, 60, 46, 10
    n = len(items)
    height = height or mt + mb + n * (row_h + gap)
    pw = width - ml - mr
    vmax = max(v for _, v in items)
    fmt = fmt or (lambda v: f"{v:,.0f}" if v >= 10 else f"{v:g}")

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
         f'<rect width="{width}" height="{height}" fill="{SURFACE}" rx="8"/>',
         f'<text x="16" y="26" {FONT} font-size="15" font-weight="600" fill="{INK}">{esc(title)}</text>']
    for i, (label, v) in enumerate(items):
        y = mt + i * (row_h + gap)
        w = (v / vmax) * pw
        p.append(f'<text x="{ml - 10}" y="{y + row_h / 2 + 4}" {FONT} font-size="12" fill="{INK2}" '
                 f'text-anchor="end">{esc(label)}</text>')
        p.append(f'<path d="{hbar_path(ml, y, w, row_h - 8)}" fill="{color}">'
                 f'<title>{esc(label)}: {fmt(v)}{unit}</title></path>')
        p.append(f'<text x="{ml + w + 8:.1f}" y="{y + row_h / 2 + 2}" {FONT} font-size="11.5" '
                 f'fill="{INK2}">{fmt(v)}{unit}</text>')
    p.append("</svg>")
    (OUT / filename).write_text("\n".join(p))
    print("wrote", filename)


def scatter(filename, title, points, xlabel, ylabel, width=760, height=420,
            xmax=None, ymin=None, ymax=None):
    """points: list of (label, x, y, color, anchor). Direct-labeled scatter."""
    ml, mr, mt, mb = 56, 30, 46, 46
    pw, ph = width - ml - mr, height - mt - mb
    xmax = xmax or max(x for _, x, _, _, _ in points) * 1.15
    ymin = ymin if ymin is not None else 0
    ymax = ymax or max(y for _, _, y, _, _ in points) * 1.1

    def X(x): return ml + (x / xmax) * pw
    def Y(y): return mt + ph - ((y - ymin) / (ymax - ymin)) * ph

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
         f'<rect width="{width}" height="{height}" fill="{SURFACE}" rx="8"/>',
         f'<text x="{ml}" y="26" {FONT} font-size="15" font-weight="600" fill="{INK}">{esc(title)}</text>']
    for t in nice_ticks(xmax):
        if t > xmax: break
        p.append(f'<line x1="{X(t):.1f}" y1="{mt}" x2="{X(t):.1f}" y2="{mt+ph}" stroke="{GRID}"/>')
        p.append(f'<text x="{X(t):.1f}" y="{mt+ph+16}" {FONT} font-size="11" fill="{MUTED}" text-anchor="middle">${t:g}</text>')
    yt = ymin
    while yt <= ymax + 1e-9:
        p.append(f'<line x1="{ml}" y1="{Y(yt):.1f}" x2="{ml+pw}" y2="{Y(yt):.1f}" stroke="{GRID}"/>')
        p.append(f'<text x="{ml-8}" y="{Y(yt)+4:.1f}" {FONT} font-size="11" fill="{MUTED}" text-anchor="end">{yt:g}</text>')
        yt += 0.5
    p.append(f'<text x="{ml + pw/2}" y="{height-8}" {FONT} font-size="11.5" fill="{INK2}" text-anchor="middle">{esc(xlabel)}</text>')
    p.append(f'<text x="16" y="{mt + ph/2}" {FONT} font-size="11.5" fill="{INK2}" '
             f'transform="rotate(-90 16 {mt + ph/2})" text-anchor="middle">{esc(ylabel)}</text>')
    for pt in points:
        label, x, y, color, anchor = pt[:5]
        dy = pt[5] if len(pt) > 5 else 0
        p.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="8" fill="{color}" stroke="{SURFACE}" stroke-width="2">'
                 f'<title>{esc(label)}: ${x}/report, quality {y}</title></circle>')
        dx = 13 if anchor == "start" else -13
        p.append(f'<text x="{X(x)+dx:.1f}" y="{Y(y)+4+dy:.1f}" {FONT} font-size="12" fill="{INK2}" '
                 f'text-anchor="{anchor}">{esc(label)}</text>')
    p.append("</svg>")
    (OUT / filename).write_text("\n".join(p))
    print("wrote", filename)


if __name__ == "__main__":
    # Example — replace with the report's real data.
    grouped_bars(
        "example-volume.svg",
        "Widgets and users per month",
        ["Jan", "Feb", "Mar"],
        [
            ("Widgets", BLUE, [10, 137, 185], MUTED),
            ("Users", AQUA, [3, 51, 53], INK2),
        ],
    )
    hbars(
        "example-breakdown.svg",
        "Items by category",
        [("alpha", 890), ("beta", 370), ("gamma", 281)],
    )
    scatter(
        "example-tradeoff.svg",
        "Quality vs cost",
        [
            ("candidate A", 0.17, 4.8, AQUA, "end"),
            ("current", 0.017, 4.1, YELLOW, "start"),
            ("candidate B", 0.096, 3.8, BLUE, "start"),
        ],
        "Cost per unit (USD)",
        "Quality rating (1-5)",
        ymin=2, ymax=5,
    )
