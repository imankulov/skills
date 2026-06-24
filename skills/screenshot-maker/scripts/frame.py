#!/usr/bin/env python3
"""Frame a screenshot with rounded corners, drop shadow, and gradient background.

Usage:
    python frame.py input.png output.png
    python frame.py input.png output.png --preset slate --trim
    python frame.py input.png output.png --radius 4 --bg-start "#2c3e50" --bg-end "#4ca1af"
    python frame.py input.png output.png --no-bg
"""

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

PRESETS = {
    "slate": ("#2c3e50", "#4ca1af"),
    "ocean": ("#667eea", "#764ba2"),
    "sunset": ("#f093fb", "#f5576c"),
    "forest": ("#11998e", "#38ef7d"),
    "ember": ("#ff9a9e", "#fecfef"),
    "midnight": ("#0f0c29", "#302b63"),
}


def frame(
    *,
    input_path: str,
    output_path: str,
    padding: int = 20,
    radius: int = 4,
    shadow_blur: int = 15,
    shadow_opacity: int = 30,
    bg_start: str = "#2c3e50",
    bg_end: str = "#4ca1af",
    bg_margin: int = 40,
    resize: str | None = None,
    no_bg: bool = False,
    trim: bool = False,
) -> None:
    """Apply professional framing to a raw screenshot.

    Pipeline: trim → pad → round corners → drop shadow → gradient background → resize.
    """
    tmpdir = Path(tempfile.mkdtemp())
    try:
        current = input_path

        if trim:
            current = step_trim(current, tmpdir)

        current = step_pad(current, tmpdir, padding)
        current = step_round_corners(current, tmpdir, radius)
        current = step_shadow(current, tmpdir, shadow_blur, shadow_opacity)

        if no_bg:
            finalize(current, output_path, resize)
            return

        current = step_gradient_bg(current, tmpdir, bg_start, bg_end, bg_margin)
        finalize(current, output_path, resize)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def step_trim(current: str, tmpdir: Path) -> str:
    """Remove whitespace borders from the image."""
    out = str(tmpdir / "trimmed.png")
    magick(current, "-trim", "+repage", out)
    return out


def step_pad(current: str, tmpdir: Path, padding: int) -> str:
    """Add uniform padding around the image."""
    out = str(tmpdir / "padded.png")
    magick(current, "-bordercolor", "white", "-border", f"{padding}x{padding}", out)
    return out


def step_round_corners(current: str, tmpdir: Path, radius: int) -> str:
    """Apply rounded corners via an alpha mask."""
    w, h = get_dimensions(current)
    mask = str(tmpdir / "mask.png")
    magick(
        "-size", f"{w}x{h}", "xc:none",
        "-fill", "white",
        "-draw", f"roundrectangle 0,0,{w - 1},{h - 1},{radius},{radius}",
        mask,
    )
    out = str(tmpdir / "rounded.png")
    magick(current, mask, "-alpha", "off", "-compose", "CopyOpacity", "-composite", out)
    return out


def step_shadow(current: str, tmpdir: Path, blur: int, opacity: int) -> str:
    """Add a drop shadow beneath the image."""
    out = str(tmpdir / "shadow.png")
    magick(
        current,
        "(", "+clone",
        "-background", f"rgba(0,0,0,0.{opacity})",
        "-shadow", f"80x{blur}+0+4",
        ")",
        "+swap", "-background", "none", "-layers", "merge", "+repage",
        out,
    )
    return out


def step_gradient_bg(current: str, tmpdir: Path, bg_start: str, bg_end: str, margin: int) -> str:
    """Create a gradient background and composite the card on top."""
    sw, sh = get_dimensions(current)
    bg_w = sw + margin * 2
    bg_h = sh + margin * 2

    bg = str(tmpdir / "bg.png")
    magick("-size", f"{bg_w}x{bg_h}", f"gradient:{bg_start}-{bg_end}", bg)

    out = str(tmpdir / "composed.png")
    magick(bg, current, "-gravity", "center", "-composite", out)
    return out


def finalize(current: str, output_path: str, resize: str | None) -> None:
    """Write the final output, optionally resizing."""
    if resize:
        magick(current, "-resize", resize, output_path)
    else:
        shutil.copy2(current, output_path)

    dims = identify(output_path, "%wx%h")
    print(f"Saved to {output_path} ({dims})")


# --- Helpers ---


def magick(*args: str) -> None:
    """Run an ImageMagick command."""
    subprocess.run(["magick", *args], check=True)


def identify(path: str, fmt: str) -> str:
    """Run magick identify and return formatted output."""
    result = subprocess.run(
        ["magick", "identify", "-format", fmt, path],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_dimensions(path: str) -> tuple[int, int]:
    """Return (width, height) of an image."""
    w, h = identify(path, "%w %h").split()
    return int(w), int(h)


# --- CLI ---


def main() -> None:
    """Parse arguments and run the framing pipeline."""
    parser = argparse.ArgumentParser(description="Frame a screenshot with professional styling")
    parser.add_argument("input", help="Input PNG path")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--padding", type=int, default=20, help="Inner padding (default: 20)")
    parser.add_argument("--radius", type=int, default=4, help="Corner radius (default: 4)")
    parser.add_argument("--shadow-blur", type=int, default=15, help="Shadow softness (default: 15)")
    parser.add_argument("--shadow-opacity", type=int, default=30, help="Shadow darkness 0-100 (default: 30)")
    parser.add_argument("--bg-start", default="#2c3e50", help="Gradient start color (default: #2c3e50)")
    parser.add_argument("--bg-end", default="#4ca1af", help="Gradient end color (default: #4ca1af)")
    parser.add_argument("--bg-margin", type=int, default=40, help="Background margin (default: 40)")
    parser.add_argument("--resize", help="Resize final image (e.g. 800x or 400x250)")
    parser.add_argument("--no-bg", action="store_true", help="Skip gradient background")
    parser.add_argument("--trim", action="store_true", help="Auto-trim whitespace first")
    parser.add_argument(
        "--preset",
        choices=PRESETS,
        help="Background gradient preset (default colors match 'slate')",
    )
    args = parser.parse_args()

    bg_start = args.bg_start
    bg_end = args.bg_end
    if args.preset:
        bg_start, bg_end = PRESETS[args.preset]

    frame(
        input_path=args.input,
        output_path=args.output,
        padding=args.padding,
        radius=args.radius,
        shadow_blur=args.shadow_blur,
        shadow_opacity=args.shadow_opacity,
        bg_start=bg_start,
        bg_end=bg_end,
        bg_margin=args.bg_margin,
        resize=args.resize,
        no_bg=args.no_bg,
        trim=args.trim,
    )


if __name__ == "__main__":
    main()
