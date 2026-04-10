# Extraction Principles

Rules for deciding what becomes a skill and what gets discarded.

## What qualifies as a skill

A skill is a **repeatable procedure** that Claude performed across multiple sessions. Not every learned fact is a skill.

### Must have ALL of:

- **Repetition**: Pattern appeared 2+ times across different sessions
- **Procedure**: Has concrete steps (not just a fact or preference)
- **Transferability**: Would help in a future session (not a one-off fix)

### Must NOT be:

- A single fact ("project uses PostgreSQL") — that's memory, not a skill
- A user preference ("use tabs not spaces") — that belongs in CLAUDE.md
- A one-time debugging session — unless the same error class recurs
- A workaround for a since-fixed bug

## Extraction heuristics

### Detect repetition by pattern, not by literal match

"User asked to run tests before committing" and "User wanted CI checks locally first" are the same pattern: pre-commit verification.

### Methodology over implementation

Prefer extracting HOW something was solved over WHAT the fix was.

- Bad: "Change line 42 in config.ts to use port 3001"
- Good: "When port conflicts occur, check running processes with `lsof -i :<port>`, identify the conflicting service, then either kill it or change the port"

### Confidence scoring

| Score   | Meaning                                                            |
| ------- | ------------------------------------------------------------------ |
| 0.0–0.3 | Weak signal — observed once, might be noise. Discard.              |
| 0.3–0.5 | Emerging — seen twice, but could be coincidence. Hold.             |
| 0.5–0.7 | Likely pattern — 2-3 occurrences with similar context. Review.     |
| 0.7–0.9 | Strong pattern — 3+ occurrences, consistent procedure. Review.     |
| 0.9–1.0 | Near-certain — well-established workflow the user repeats. Review. |

Only skills with confidence >= 0.5 go to `review/`.

### Scope detection

- References specific file paths, project configs, or repo names → `project`
- References general tools, languages, or universal patterns → `global`
- When in doubt, mark `project` — it's safer to under-scope

## Anti-patterns

### Don't extract obvious things

"Run `npm install` before `npm start`" — Claude already knows this.

### Don't extract from failed sessions

If the user abandoned an approach or Claude went in circles, that's not a skill — it's a cautionary tale at best.

### Don't merge unrelated patterns

Two different debugging techniques that happened to occur in the same session are two separate skills, not one.

### Don't over-abstract

"Always verify before acting" is too vague to be useful. Keep skills grounded in concrete procedures with specific triggers.
