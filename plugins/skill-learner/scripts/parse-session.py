#!/usr/bin/env python3
"""Parse a Claude Code session JSONL into a condensed summary for skill extraction.

Usage: python3 parse-session.py <session-jsonl-path>
       python3 parse-session.py --recent [--project <project-dir-name>] [--limit N]

Outputs JSON with condensed session data: user requests, tool usage patterns,
errors encountered, and resolutions.
"""

import json
import os
import sys
from pathlib import Path


def parse_message_content(content):
    """Extract readable text from message content (string or block list)."""
    if isinstance(content, str):
        return content[:500]
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block["text"][:300])
                elif block.get("type") == "tool_use":
                    inp = block.get("input", {})
                    # Summarize tool calls compactly
                    if block["name"] == "Bash":
                        parts.append(f"[Tool: Bash] {inp.get('command', '')[:200]}")
                    elif block["name"] in ("Read", "Glob", "Grep"):
                        parts.append(f"[Tool: {block['name']}] {inp.get('file_path', inp.get('pattern', ''))[:200]}")
                    elif block["name"] in ("Edit", "Write"):
                        parts.append(f"[Tool: {block['name']}] {inp.get('file_path', '')[:200]}")
                    else:
                        parts.append(f"[Tool: {block['name']}]")
                elif block.get("type") == "tool_result":
                    result_text = str(block.get("content", ""))[:200]
                    is_error = block.get("is_error", False)
                    if is_error:
                        parts.append(f"[Error] {result_text}")
                    elif "error" in result_text.lower() or "exit code" in result_text.lower():
                        parts.append(f"[Result] {result_text}")
        return "\n".join(parts)
    return ""


def parse_session(path: Path) -> dict:
    """Parse a session JSONL file into a condensed summary."""
    messages = []
    tools_used = {}
    errors = []
    user_requests = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = entry.get("type")
            if msg_type not in ("user", "assistant"):
                continue

            content = entry.get("message", {}).get("content") if isinstance(entry.get("message"), dict) else entry.get("content")
            if not content:
                continue

            parsed = parse_message_content(content)
            if not parsed:
                continue

            # Track user requests (non-tool-result messages)
            if msg_type == "user" and isinstance(content, str):
                user_requests.append(parsed[:300])

            # Track tool usage
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        name = block["name"]
                        tools_used[name] = tools_used.get(name, 0) + 1
                    if isinstance(block, dict) and block.get("type") == "tool_result" and block.get("is_error"):
                        errors.append(str(block.get("content", ""))[:300])

            messages.append({"role": msg_type, "content": parsed})

    # Condense: keep first 5 + last 10 messages if too long
    if len(messages) > 30:
        messages = messages[:5] + [{"role": "system", "content": f"... ({len(messages) - 15} messages omitted) ..."}] + messages[-10:]

    return {
        "session_id": path.stem,
        "file": str(path),
        "message_count": len(messages),
        "user_requests": user_requests[:10],
        "tools_used": tools_used,
        "errors": errors[:10],
        "messages": messages,
    }


def find_recent_sessions(project_name: str | None = None, limit: int = 5) -> list[Path]:
    """Find the N most recent session JSONL files."""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.is_dir():
        return []

    jsonl_files = []
    search_dirs = [projects_dir / project_name] if project_name else list(projects_dir.iterdir())

    for pdir in search_dirs:
        if not pdir.is_dir():
            continue
        for f in pdir.glob("*.jsonl"):
            jsonl_files.append(f)

    # Sort by modification time, most recent first
    jsonl_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return jsonl_files[:limit]


def main():
    if len(sys.argv) < 2:
        print("Usage: parse-session.py <path> | --recent [--project NAME] [--limit N]", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--recent":
        project = None
        limit = 5
        args = sys.argv[2:]
        while args:
            if args[0] == "--project" and len(args) > 1:
                project = args[1]
                args = args[2:]
            elif args[0] == "--limit" and len(args) > 1:
                limit = int(args[1])
                args = args[2:]
            else:
                args = args[1:]

        paths = find_recent_sessions(project, limit)
        if not paths:
            print("[]")
            return

        sessions = [parse_session(p) for p in paths]
        json.dump(sessions, sys.stdout, indent=2)
    else:
        path = Path(sys.argv[1])
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            sys.exit(1)
        result = parse_session(path)
        json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
