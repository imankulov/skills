#!/usr/bin/env python3
"""Browser-side screenshot preparation: crop elements, blur content, hide chrome, highlight.

Shells out to agent-browser for all browser interaction.

Usage:
    python prepare.py crop --selector "section.hero" --output /tmp/raw.png
    python prepare.py blur --text "secret phrase"
    python prepare.py blur --selector ".api-key" --radius 8
    python prepare.py highlight --selector ".feature-card" --mode spotlight
    python prepare.py highlight --selector ".cta-button" --mode border --color red
    python prepare.py hide-chrome
    python prepare.py hide --selector "nav, footer, .cookie-banner"
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def crop(args: argparse.Namespace) -> None:
    """Screenshot an element, falling back to viewport crop if the result is blank."""
    selector = args.selector
    output = args.output

    run_ab("scrollintoview", selector)

    box = parse_box(run_ab("get", "box", selector))
    if not all(k in box for k in ("x", "y", "width", "height")):
        print(f"Could not get bounding box for '{selector}'", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_element = f.name
    run_ab("screenshot", selector, tmp_element)

    if not is_blank_image(tmp_element):
        Path(tmp_element).rename(output)
        print(f"Saved element screenshot to {output}")
        return

    Path(tmp_element).unlink(missing_ok=True)
    print("Element screenshot was blank, falling back to viewport crop", file=sys.stderr)
    crop_via_viewport(selector, output)


def blur(args: argparse.Namespace) -> None:
    """Blur elements or text on the page via CSS filter injection."""
    radius = args.radius

    if args.selector:
        js = f"""
            (() => {{
                document.querySelectorAll({json.dumps(args.selector)}).forEach(el => {{
                    el.style.filter = 'blur({radius}px)';
                    el.style.userSelect = 'none';
                }});
                return document.querySelectorAll({json.dumps(args.selector)}).length;
            }})();
        """
        count = eval_js(js).strip().strip('"')
        print(f"Blurred {count} element(s) matching '{args.selector}'")

    elif args.text:
        js = f"""
            (() => {{
                const text = {json.dumps(args.text)};
                const regex = new RegExp(text.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&'), 'g');
                let count = 0;
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                const nodes = [];
                while (walker.nextNode()) {{
                    if (walker.currentNode.textContent.includes(text)) {{
                        nodes.push(walker.currentNode);
                    }}
                }}
                nodes.forEach(node => {{
                    const span = document.createElement('span');
                    span.innerHTML = node.textContent.replace(
                        regex,
                        '<span style="filter:blur({radius}px);user-select:none">' + text + '</span>'
                    );
                    node.parentNode.replaceChild(span, node);
                    count++;
                }});
                return count;
            }})();
        """
        count = eval_js(js).strip().strip('"')
        print(f"Blurred {count} text occurrence(s) of '{args.text}'")
    else:
        print("Provide --text or --selector", file=sys.stderr)
        sys.exit(1)


def highlight(args: argparse.Namespace) -> None:
    """Inject a highlight overlay (border or spotlight) around an element."""
    selector = args.selector
    mode = args.mode
    color = args.color
    padding = args.padding
    radius = args.border_radius
    thickness = args.thickness
    opacity = args.opacity

    if mode == "spotlight":
        js = f"""
            (() => {{
                const els = document.querySelectorAll({json.dumps(selector)});
                if (!els.length) return JSON.stringify({{error: 'no elements found'}});

                let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
                els.forEach(el => {{
                    const r = el.getBoundingClientRect();
                    minX = Math.min(minX, r.left);
                    minY = Math.min(minY, r.top);
                    maxX = Math.max(maxX, r.right);
                    maxY = Math.max(maxY, r.bottom);
                }});

                const pad = {padding};
                const spot = document.createElement('div');
                spot.style.cssText = [
                    'position: fixed',
                    'top: ' + (minY - pad) + 'px',
                    'left: ' + (minX - pad) + 'px',
                    'width: ' + (maxX - minX + pad * 2) + 'px',
                    'height: ' + (maxY - minY + pad * 2) + 'px',
                    'border-radius: {radius}px',
                    'box-shadow: 0 0 0 99999px rgba(0, 0, 0, {opacity})',
                    'z-index: 99998',
                    'pointer-events: none',
                ].join('; ');
                document.body.appendChild(spot);
                return els.length;
            }})();
        """
        result = eval_js(js).strip().strip('"')
        print(f"Spotlight on {result} element(s) matching '{selector}'")

    elif mode == "border":
        js = f"""
            (() => {{
                const els = document.querySelectorAll({json.dumps(selector)});
                if (!els.length) return JSON.stringify({{error: 'no elements found'}});

                els.forEach(el => {{
                    const r = el.getBoundingClientRect();
                    const pad = {padding};
                    const border = document.createElement('div');
                    border.style.cssText = [
                        'position: fixed',
                        'top: ' + (r.top - pad) + 'px',
                        'left: ' + (r.left - pad) + 'px',
                        'width: ' + (r.width + pad * 2) + 'px',
                        'height: ' + (r.height + pad * 2) + 'px',
                        'border: {thickness}px solid {color}',
                        'border-radius: {radius}px',
                        'z-index: 99998',
                        'pointer-events: none',
                    ].join('; ');
                    document.body.appendChild(border);
                }});
                return els.length;
            }})();
        """
        result = eval_js(js).strip().strip('"')
        print(f"Border on {result} element(s) matching '{selector}'")


def hide_chrome(args: argparse.Namespace) -> None:
    """Hide common page chrome (nav, footer, sticky banners)."""
    js = """
        (() => {
            const selectors = [
                'nav', 'header', 'footer',
                '[class*="navbar"]', '[class*="nav-bar"]',
                '[class*="cookie"]', '[class*="consent"]',
                '[class*="banner"]', '[class*="popup"]',
                '[class*="modal"]', '[class*="overlay"]',
                '[role="navigation"]', '[role="banner"]',
                '[class*="sticky"]', '[class*="fixed"]',
            ];
            let count = 0;
            selectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => {
                    const pos = getComputedStyle(el).position;
                    if (pos === 'fixed' || pos === 'sticky' || el.tagName === 'NAV' ||
                        el.tagName === 'HEADER' || el.tagName === 'FOOTER') {
                        el.style.setProperty('display', 'none', 'important');
                        count++;
                    }
                });
            });
            return count;
        })();
    """
    count = eval_js(js).strip().strip('"')
    print(f"Hidden {count} chrome element(s)")


def hide(args: argparse.Namespace) -> None:
    """Hide specific elements by CSS selector."""
    js = f"""
        (() => {{
            const els = document.querySelectorAll({json.dumps(args.selector)});
            els.forEach(el => el.style.setProperty('display', 'none', 'important'));
            return els.length;
        }})();
    """
    count = eval_js(js).strip().strip('"')
    print(f"Hidden {count} element(s) matching '{args.selector}'")


# --- Helpers ---


def run_ab(*args: str) -> str:
    """Run an agent-browser command and return stdout."""
    result = subprocess.run(
        ["agent-browser", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"agent-browser error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def eval_js(script: str) -> str:
    """Evaluate JavaScript in the browser via agent-browser eval --stdin."""
    result = subprocess.run(
        ["agent-browser", "eval", "--stdin"],
        input=script,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"eval error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def parse_box(output: str) -> dict[str, float]:
    """Parse agent-browser 'get box' output into a dict of coordinates."""
    box = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            key = parts[0].rstrip(":")
            try:
                box[key] = float(parts[1])
            except ValueError:
                pass
    return box


def is_blank_image(path: str) -> bool:
    """Check if an image is a single solid color."""
    check = subprocess.run(
        ["magick", path, "-format", "%[fx:standard_deviation]", "info:"],
        capture_output=True,
        text=True,
    )
    try:
        return float(check.stdout.strip()) <= 0.01
    except ValueError:
        return True


def crop_via_viewport(selector: str, output: str) -> None:
    """Scroll element into view, take viewport screenshot, crop to element bounds."""
    eval_js(f"""
        (() => {{
            const el = document.querySelector({json.dumps(selector)});
            if (el) el.scrollIntoView({{block: 'start'}});
        }})();
    """)
    run_ab("wait", "300")

    box = parse_box(run_ab("get", "box", selector))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_vp = f.name
    run_ab("screenshot", tmp_vp)

    vp_info = subprocess.run(
        ["magick", "identify", "-format", "%w %h", tmp_vp],
        capture_output=True,
        text=True,
    )
    vp_w, vp_h = map(int, vp_info.stdout.strip().split())

    css_viewport_width = float(eval_js("window.innerWidth").strip().strip('"'))
    scale = vp_w / css_viewport_width if css_viewport_width > 0 else 1

    x = max(0, int(box["x"] * scale))
    y = max(0, int(box["y"] * scale))
    w = min(int(box["width"] * scale), vp_w - x)
    h = min(int(box["height"] * scale), vp_h - y)

    subprocess.run(
        ["magick", tmp_vp, "-crop", f"{w}x{h}+{x}+{y}", "+repage", output],
        check=True,
    )
    Path(tmp_vp).unlink(missing_ok=True)

    dims = subprocess.run(
        ["magick", "identify", "-format", "%wx%h", output],
        capture_output=True,
        text=True,
    )
    print(f"Saved viewport crop to {output} ({dims.stdout.strip()})")


# --- CLI ---


def main() -> None:
    parser = argparse.ArgumentParser(description="Screenshot preparation tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_crop = sub.add_parser("crop", help="Screenshot an element (with viewport-crop fallback)")
    p_crop.add_argument("--selector", required=True, help="CSS selector for the element")
    p_crop.add_argument("--output", required=True, help="Output PNG path")
    p_crop.set_defaults(func=crop)

    p_blur = sub.add_parser("blur", help="Blur text or elements on the page")
    p_blur.add_argument("--text", help="Text string to blur")
    p_blur.add_argument("--selector", help="CSS selector for elements to blur")
    p_blur.add_argument("--radius", type=int, default=5, help="Blur radius in px (default: 5)")
    p_blur.set_defaults(func=blur)

    p_hl = sub.add_parser("highlight", help="Highlight an element (spotlight or border)")
    p_hl.add_argument("--selector", required=True, help="CSS selector for element(s) to highlight")
    p_hl.add_argument("--mode", choices=["spotlight", "border"], default="border",
                       help="spotlight: dim everything else; border: colored outline (default: border)")
    p_hl.add_argument("--color", default="#ef4444", help="Border color (default: #ef4444, a red)")
    p_hl.add_argument("--padding", type=int, default=6, help="Space between element and highlight (default: 6)")
    p_hl.add_argument("--border-radius", type=int, default=4, help="Corner radius (default: 4)")
    p_hl.add_argument("--thickness", type=int, default=3, help="Border thickness for border mode (default: 3)")
    p_hl.add_argument("--opacity", type=float, default=0.5, help="Overlay opacity for spotlight mode (default: 0.5)")
    p_hl.set_defaults(func=highlight)

    p_hc = sub.add_parser("hide-chrome", help="Hide common page chrome (nav, footer, banners)")
    p_hc.set_defaults(func=hide_chrome)

    p_hide = sub.add_parser("hide", help="Hide specific elements by selector")
    p_hide.add_argument("--selector", required=True, help="CSS selector for elements to hide")
    p_hide.set_defaults(func=hide)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
