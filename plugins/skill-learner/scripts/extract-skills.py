#!/usr/bin/env python3
"""Background skill extraction from session data.

Called by the Stop hook. Reads the current session's JSONL,
parses it, and spawns a Claude subprocess to analyze patterns
and write skill files to ~/.claude/skills/review/.

Usage: python3 extract-skills.py <session-jsonl-path>
"""

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent
REVIEW_DIR = Path.home() / ".claude" / "skills" / "review"
ACTIVE_DIR = Path.home() / ".claude" / "skills" / "active"
REJECTED_DIR = Path.home() / ".claude" / "skills" / "rejected"
STATE_DIR = Path.home() / ".claude" / "skills" / ".state"
PROCESSED_FILE = STATE_DIR / "processed-sessions.txt"

# Minimum message count to consider a session worth analyzing
MIN_MESSAGES = 10


def is_processed(session_id: str) -> bool:
    """Check if this session was already processed."""
    if not PROCESSED_FILE.exists():
        return False
    return session_id in PROCESSED_FILE.read_text()


def mark_processed(session_id: str):
    """Mark a session as processed."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, "a") as f:
        f.write(f"{session_id}\n")


def existing_skill_names() -> set[str]:
    """Get names of all existing skills (active, review, rejected)."""
    names = set()
    for d in (REVIEW_DIR, ACTIVE_DIR, REJECTED_DIR):
        if d.is_dir():
            names.update(p.stem for p in d.glob("*.md"))
    return names


def build_prompt(session_data: dict, existing: set[str]) -> str:
    """Build the extraction prompt for Claude."""
    extraction_principles = (PLUGIN_ROOT / "references" / "extraction-principles.md").read_text()
    skill_format = (PLUGIN_ROOT / "references" / "skill-format.md").read_text()

    existing_list = ", ".join(sorted(existing)) if existing else "(none)"

    return f"""You are a skill extraction agent. Analyze this coding session and identify
repeatable procedures that could become reusable skills.

## Session Data

```json
{json.dumps(session_data, indent=2)[:50000]}
```

## Existing skills (do NOT duplicate these)

{existing_list}

## Extraction Principles

{extraction_principles}

## Skill Format

{skill_format}

## Instructions

1. Analyze the session for repeatable procedures (debugging patterns, workflow steps, tool usage patterns)
2. For each potential skill, assess confidence based on the principles above
3. Only extract skills with confidence >= 0.5
4. Output ONLY valid JSON — an array of skill objects. No markdown, no explanation.

Output format:
```json
[
  {{
    "name": "skill-name-here",
    "filename": "skill-name-here.md",
    "content": "---\\nname: skill-name-here\\n..."
  }}
]
```

If no skills worth extracting, output: []
"""


def run_extraction(session_path: Path):
    """Run the full extraction pipeline."""
    # Import parse_session from sibling script
    sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))
    from importlib import import_module
    parse_mod = import_module("parse-session")
    session_data = parse_mod.parse_session(session_path)

    session_id = session_data["session_id"]

    # Skip if already processed
    if is_processed(session_id):
        return

    # Skip trivial sessions
    if session_data["message_count"] < MIN_MESSAGES:
        mark_processed(session_id)
        return

    existing = existing_skill_names()
    prompt = build_prompt(session_data, existing)

    # Spawn Claude CLI to analyze
    try:
        result = subprocess.run(
            ["claude", "--model", "haiku", "-p", prompt, "--no-input"],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        mark_processed(session_id)
        return

    if result.returncode != 0:
        mark_processed(session_id)
        return

    # Parse output — find JSON array in response
    output = result.stdout.strip()

    # Try to extract JSON from the response
    try:
        # Try direct parse first
        skills = json.loads(output)
    except json.JSONDecodeError:
        # Try to find JSON array in the output
        start = output.find("[")
        end = output.rfind("]")
        if start == -1 or end == -1:
            mark_processed(session_id)
            return
        try:
            skills = json.loads(output[start:end + 1])
        except json.JSONDecodeError:
            mark_processed(session_id)
            return

    if not isinstance(skills, list) or not skills:
        mark_processed(session_id)
        return

    # Write skills to review/
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for skill in skills:
        name = skill.get("name", "")
        content = skill.get("content", "")
        if not name or not content:
            continue
        # Skip if already exists anywhere
        if name in existing:
            continue
        filepath = REVIEW_DIR / f"{name}.md"
        if not filepath.exists():
            filepath.write_text(content)

    mark_processed(session_id)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract-skills.py <session-jsonl-path>", file=sys.stderr)
        sys.exit(1)

    session_path = Path(sys.argv[1])
    if not session_path.exists():
        sys.exit(0)

    run_extraction(session_path)


if __name__ == "__main__":
    main()
