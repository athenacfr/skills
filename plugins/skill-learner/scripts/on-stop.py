#!/usr/bin/env python3
"""Stop hook handler. Finds the current session JSONL and spawns
background extraction. Produces zero stdout (zero token cost)."""

import os
import subprocess
import sys
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent
EXTRACT_SCRIPT = PLUGIN_ROOT / "scripts" / "extract-skills.py"


def find_current_session() -> Path | None:
    """Find the most recently modified session JSONL file."""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.is_dir():
        return None

    latest = None
    latest_mtime = 0

    for pdir in projects_dir.iterdir():
        if not pdir.is_dir():
            continue
        for f in pdir.glob("*.jsonl"):
            mtime = f.stat().st_mtime
            if mtime > latest_mtime:
                latest = f
                latest_mtime = mtime

    return latest


def main():
    session = find_current_session()
    if not session:
        sys.exit(0)

    # Spawn extraction in background — don't block the session ending
    subprocess.Popen(
        [sys.executable, str(EXTRACT_SCRIPT), str(session)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Zero output — no token cost
    sys.exit(0)


if __name__ == "__main__":
    main()
