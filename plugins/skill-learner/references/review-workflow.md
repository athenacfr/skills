# Review Workflow

How pending skills move from `review/` to active or get discarded.

## Folder Layout

```
~/.claude/skills/
├── review/              # Pending skills awaiting user approval
│   ├── fix-prisma-migrations.md
│   └── react-form-patterns.md
├── active/              # Approved skills (loaded by Claude Code)
│   ├── debug-port-conflicts.md
│   └── git-rebase-workflow.md
└── rejected/            # Discarded skills (kept for dedup, never loaded)
    └── stale-cache-fix.md
```

## Review actions

For each pending skill, the user can:

| Action             | What happens                                    |
| ------------------ | ----------------------------------------------- |
| **approve**        | Move from `review/` to `active/`                |
| **edit + approve** | User modifies the skill, then move to `active/` |
| **reject**         | Move from `review/` to `rejected/`              |
| **skip**           | Leave in `review/` for later                    |

## Review presentation

When reviewing, show for each skill:

1. **Name** and **confidence score**
2. **Occurrences** — how many times the pattern was seen
3. **Scope** — project or global
4. **Procedure summary** — the key steps (not the full file)
5. **Source sessions** — when this was observed

Let the user batch-review: "approve all with confidence > 0.8" or review one by one.

## Deduplication

Before placing a new skill in `review/`:

1. Check `active/` — if a similar skill exists, skip (or update its occurrence count)
2. Check `rejected/` — if it was previously rejected, don't re-propose unless confidence increased significantly (> 0.2 delta)
3. Check `review/` — if already pending, merge occurrences and update confidence

## Skill lifecycle

```
Session observation
       ↓
  Pattern detected (2+ occurrences, confidence >= 0.5)
       ↓
  Dedup check (active? rejected? already pending?)
       ↓
  Write to review/
       ↓
  SessionStart hook notifies user
       ↓
  User runs /skill-learner:review
       ↓
  approve → active/    reject → rejected/    skip → stays in review/
```
