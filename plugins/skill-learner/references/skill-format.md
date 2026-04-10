# Skill Format

Generated skills are Markdown files placed in `~/.claude/skills/review/`. Each file is a self-contained skill that, once approved, moves to `~/.claude/skills/`.

## File Structure

```
<skill-name>.md
```

Filename: kebab-case, descriptive, no prefix. Example: `fix-prisma-migrations.md`, `react-form-patterns.md`.

## Template

```markdown
---
name: <skill-name>
description: <when to trigger — specific phrases and contexts>
confidence: <0.0-1.0>
sources:
  - <session-id or date that contributed>
occurrences: <number of times pattern was observed>
extracted: <YYYY-MM-DD>
scope: <project|global>
---

# <Skill Title>

<One-line summary of what this skill does.>

## When to Use

<Specific triggers: what the user says, what context looks like, what tools are being used.>

## Procedure

<Step-by-step instructions. Numbered steps. Each step is an atomic action.>

1. ...
2. ...
3. ...

## Gotchas

<Known edge cases, pitfalls, or things to watch out for. Omit if none.>
```

## Frontmatter Fields

| Field         | Required | Description                                               |
| ------------- | -------- | --------------------------------------------------------- |
| `name`        | yes      | Kebab-case identifier, matches filename                   |
| `description` | yes      | Trigger description — when should this skill activate     |
| `confidence`  | yes      | 0.0–1.0 how confident the extraction is (0.5+ for review) |
| `sources`     | yes      | Session IDs or dates where the pattern was observed       |
| `occurrences` | yes      | How many times the pattern appeared across sessions       |
| `extracted`   | yes      | Date the skill was generated                              |
| `scope`       | yes      | `project` (specific to one repo) or `global` (universal)  |

## Content Principles

### Procedure must be actionable

Every step should be something Claude can execute. No vague instructions like "handle the edge cases" — specify which edge cases and how.

### Trigger must be specific

Bad: "Use when working with databases"
Good: "Use when user says 'fix migration', 'prisma migrate', or when a Prisma migration error appears in tool output"

### Scope determines placement

- `project` skills include repo-specific paths, tools, conventions
- `global` skills are stack/project agnostic — reusable anywhere

### Strip project-specific secrets

Never include API keys, internal URLs, credentials, or sensitive paths. Generalize with placeholders if needed.
