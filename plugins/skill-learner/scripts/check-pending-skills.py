#!/usr/bin/env python3

import os
from pathlib import Path

review_dir = Path.home() / ".claude" / "skills" / "review"

if not review_dir.is_dir():
    raise SystemExit(0)

skills = sorted(p.stem for p in review_dir.glob("*.md"))

if not skills:
    raise SystemExit(0)

count = len(skills)
print(f"You have {count} pending skill(s) to review:\n")
for skill in skills:
    print(f"  - {skill}")
print("\nRun /skill-learner:review to review and enable them.")
