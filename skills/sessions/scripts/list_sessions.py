#!/usr/bin/env python3
"""List Claude Code sessions for a given project directory."""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"


@dataclass
class SessionInfo:
    session_id: str
    first_message: str
    first_timestamp: str | None
    last_timestamp: str | None
    size_kb: int
    user_turns: int
    assistant_turns: int


def list_sessions(cwd: str, *, show_all: bool = False) -> list[SessionInfo]:
    """List sessions for a project directory, sorted by start time (newest first)."""
    mangled = _mangle_cwd(cwd)
    project_dir = PROJECTS_DIR / mangled

    if not project_dir.is_dir():
        return []

    sessions = [_parse_session(f) for f in project_dir.glob("*.jsonl")]
    sessions.sort(key=lambda s: s.first_timestamp or "", reverse=True)

    if not show_all:
        sessions = sessions[:20]

    return sessions


def format_table(sessions: list[SessionInfo]) -> str:
    """Format sessions as a markdown table."""
    if not sessions:
        return "No sessions found."

    lines = ["| # | Started | Duration | Turns | Size | First message | Session ID |"]
    lines.append("|---|---------|----------|-------|------|---------------|------------|")

    for i, s in enumerate(sessions, 1):
        if s.first_timestamp:
            started = datetime.fromisoformat(s.first_timestamp).astimezone().strftime("%Y-%m-%d %H:%M")
        else:
            started = "?"

        if s.first_timestamp and s.last_timestamp:
            duration = _format_duration(s.first_timestamp, s.last_timestamp)
        else:
            duration = "?"

        msg = _truncate_message(s.first_message)
        turns = f"{s.user_turns}u/{s.assistant_turns}a"
        size = f"{s.size_kb}KB"
        lines.append(f"| {i} | {started} | {duration} | {turns} | {size} | {msg} | `{s.session_id}` |")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="List Claude Code sessions for a project.")
    parser.add_argument("cwd", nargs="?", help="Project directory (default: current directory)")
    parser.add_argument("--all", action="store_true", help="Show all sessions (default: last 20)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args()

    cwd = args.cwd or os.getcwd()
    sessions = list_sessions(cwd, show_all=args.all)

    if args.as_json:
        json.dump([asdict(s) for s in sessions], sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(format_table(sessions))


# --- internal helpers ---


def _mangle_cwd(cwd: str) -> str:
    """Converts a directory path to the mangled form used by Claude Code."""
    return cwd.replace("/", "-")


def _parse_session(session_path: Path) -> SessionInfo:
    """Parses a session JSONL file in a single pass."""
    first_message = None
    first_timestamp = None
    last_timestamp = None
    user_turns = 0
    assistant_turns = 0

    with open(session_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts = entry.get("timestamp")
            if ts:
                if first_timestamp is None:
                    first_timestamp = ts
                last_timestamp = ts

            entry_type = entry.get("type")
            if entry_type == "user":
                user_turns += 1
                if first_message is None:
                    first_message = _extract_text(entry)
            elif entry_type == "assistant":
                assistant_turns += 1

    stat = session_path.stat()
    return SessionInfo(
        session_id=session_path.stem,
        first_message=first_message or "",
        first_timestamp=first_timestamp,
        last_timestamp=last_timestamp,
        size_kb=round(stat.st_size / 1024),
        user_turns=user_turns,
        assistant_turns=assistant_turns,
    )


def _extract_text(entry: dict) -> str | None:
    """Extracts the text content from a user message entry."""
    msg = entry.get("message", {})
    if not isinstance(msg, dict):
        return None
    content = msg.get("content", "")
    if isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                return block["text"]
    elif isinstance(content, str):
        return content
    return None


def _format_duration(start_iso: str, end_iso: str) -> str:
    """Formats the duration between two ISO timestamps as a human-readable string."""
    total_seconds = int(
        (datetime.fromisoformat(end_iso) - datetime.fromisoformat(start_iso)).total_seconds()
    )

    if total_seconds < 60:
        return f"{total_seconds}s"

    minutes = total_seconds // 60
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    remaining_minutes = minutes % 60
    if hours < 24:
        return f"{hours}h{remaining_minutes}m" if remaining_minutes else f"{hours}h"

    days = hours // 24
    remaining_hours = hours % 24
    return f"{days}d{remaining_hours}h" if remaining_hours else f"{days}d"


def _truncate_message(msg: str, *, max_length: int = 60) -> str:
    """Cleans and truncates a message for table display."""
    msg = re.sub(r"<[^>]+>", "", msg)
    msg = msg.replace("\n", " ").strip()
    if len(msg) > max_length:
        msg = msg[: max_length - 3] + "..."
    return msg.replace("|", "\\|")


if __name__ == "__main__":
    main()
