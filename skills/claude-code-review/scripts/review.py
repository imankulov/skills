#!/usr/bin/env python3
"""Run Claude Code's bundled /code-review command non-interactively."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_TIMEOUT_SECONDS = 1_200
REVIEW_STANDARD = """Prioritize concrete defects introduced by the reviewed changes:
incorrect behavior, regressions, security problems, data loss, races, broken error
handling, compatibility breaks, and meaningful performance failures. Require a
reachable failure path and cite the narrowest useful line. Skip style preferences,
speculative concerns, and generic requests for more tests. An empty findings list is
valid when no actionable defect exists."""


def run_git(*args: str, cwd: Path, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(detail or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def repository_root(cwd: Path) -> Path:
    return Path(run_git("rev-parse", "--show-toplevel", cwd=cwd))


def ref_exists(ref: str, *, cwd: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def default_base(cwd: Path) -> str:
    remote_head = run_git(
        "symbolic-ref",
        "--quiet",
        "--short",
        "refs/remotes/origin/HEAD",
        cwd=cwd,
        check=False,
    )
    candidates = [remote_head, "origin/main", "origin/master", "main", "master"]
    for candidate in candidates:
        if candidate and ref_exists(candidate, cwd=cwd):
            return candidate
    raise RuntimeError("could not infer a base ref; pass --base or --target")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Claude Code's bundled /code-review command."
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--base", help="Base ref; reviews <base>...HEAD")
    scope.add_argument(
        "--target",
        help="Exact /code-review target: path, PR, branch, or ref range",
    )
    parser.add_argument("--focus", help="Extra guidance for the review subagent")
    parser.add_argument("--model", default="opus", help="Claude model alias or ID")
    parser.add_argument(
        "--effort",
        default="high",
        choices=("low", "medium", "high", "xhigh", "max"),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Subprocess timeout in seconds (default: 1200)",
    )
    parser.add_argument(
        "--max-budget-usd",
        type=float,
        help="Optional Claude Code API-spend cap",
    )
    parser.add_argument("--output", type=Path, help="Write the review to this text file")
    parser.add_argument(
        "--bypass-permissions",
        action="store_true",
        help="Use --dangerously-skip-permissions (trusted sandboxes only)",
    )
    return parser.parse_args()


def main() -> int:
    if os.environ.get("CLAUDECODE"):
        raise SystemExit(
            "error: running inside Claude Code; use the /code-review skill directly instead"
        )
    args = parse_args()
    if args.timeout <= 0:
        raise SystemExit("error: --timeout must be positive")
    if args.max_budget_usd is not None and args.max_budget_usd <= 0:
        raise SystemExit("error: --max-budget-usd must be positive")
    if shutil.which("claude") is None:
        raise SystemExit("error: claude CLI is not installed or not on PATH")

    try:
        root = repository_root(Path.cwd())
        if args.target:
            target = args.target
        else:
            base = args.base or default_base(root)
            if not ref_exists(base, cwd=root):
                raise RuntimeError(f"base ref does not resolve to a commit: {base}")
            target = f"{base}...HEAD"
    except RuntimeError as error:
        raise SystemExit(f"error: {error}") from error

    subagent_prompt = REVIEW_STANDARD
    if args.focus:
        subagent_prompt += f"\n\nPay particular attention to: {args.focus}"

    command = [
        "claude",
        "-p",
        f"/code-review {args.effort} {target}",
        "--model",
        args.model,
        "--effort",
        args.effort,
        "--append-subagent-system-prompt",
        subagent_prompt,
        "--output-format",
        "json",
        "--no-session-persistence",
    ]
    if args.bypass_permissions:
        command.append("--dangerously-skip-permissions")
    else:
        command.extend(("--permission-mode", "plan"))
    if args.max_budget_usd is not None:
        command.extend(("--max-budget-usd", str(args.max_budget_usd)))

    try:
        result = subprocess.run(
            command,
            cwd=root,
            check=False,
            stdout=subprocess.PIPE,
            text=True,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as error:
        raise SystemExit(
            f"error: Claude Code review exceeded {args.timeout} seconds"
        ) from error
    except KeyboardInterrupt:
        print("review interrupted", file=sys.stderr)
        return 130

    if result.returncode != 0:
        detail = result.stdout.strip()
        raise SystemExit(f"error: Claude Code review failed: {detail}")

    try:
        envelope = json.loads(result.stdout)
        review = envelope["result"]
        if not isinstance(review, str) or not review.strip():
            raise ValueError("empty result")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise SystemExit(
            "error: Claude Code returned no review text\n" + result.stdout
        ) from error

    rendered = review.rstrip() + "\n"
    if args.output:
        output_path = args.output.expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(output_path)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
