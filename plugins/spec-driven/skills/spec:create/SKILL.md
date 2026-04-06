---
name: spec:create
description: Create feature specs and resolve gray areas. Captures WHAT to build with testable, traceable requirements, then discusses ambiguous areas to lock implementation decisions. Produces spec.md and context.md. Use when (1) Starting new projects (initialize vision, goals, roadmap), (2) Working with existing codebases (map stack, architecture, conventions), (3) Specifying features (requirements, acceptance criteria), (4) Discussing gray areas and ambiguous behavior, (5) Tracking decisions/blockers/deferred ideas, (6) Pausing/resuming work. Triggers on "specify feature", "define requirements", "discuss feature", "how should this work", "initialize project", "map codebase", "pause work", "resume work". After completing, recommend user runs /compact then /spec:design (if complex) or /spec:run <feature>.
license: MIT
metadata:
  author: Athena Freitas - github.com/athenacfr
  version: 1.0.0
---

# Spec: Create

Create feature specs and resolve gray areas. Zero ceremony.

```
┌──────────────┐        ┌──────────────┐        ┌──────────┐
│ /spec:create │ ─/compact─▸ │ /spec:design │ ─/compact─▸ │ /spec:run│
└──────────────┘        └──────────────┘        └──────────┘
  specify + discuss        architecture           tasks + implement
  (this skill)             (if complex)            (always)
```

**After this skill completes, recommend the user runs `/compact` before moving to the next skill.**

## What This Skill Does

1. **Specify** — Capture requirements with testable acceptance criteria, priority levels, and requirement IDs. See [specify.md](references/specify.md).
2. **Discuss** — When gray areas are detected (ambiguous user-facing behavior), walk through them with the user and lock decisions in `context.md`. See [discuss.md](references/discuss.md).

### Outputs

- `.specs/features/<feature>/spec.md` — requirements with traceable IDs
- `.specs/features/<feature>/context.md` — user decisions for gray areas (only when needed)

## Auto-Sizing

| Scope       | What                     | This Skill                   | Next Step                          |
| ----------- | ------------------------ | ---------------------------- | ---------------------------------- |
| **Small**   | ≤3 files, one sentence   | Skip — go straight to        | `/spec:run` quick mode             |
| **Medium**  | Clear feature, <10 tasks | Spec (brief), no discuss     | `/compact` → `/spec:run <feature>` |
| **Large**   | Multi-component feature  | Full spec, discuss if needed | `/compact` → `/spec:design`        |
| **Complex** | Ambiguity, new domain    | Full spec + discuss          | `/compact` → `/spec:design`        |

## Project Structure

```
.specs/
├── project/
│   ├── PROJECT.md      # Vision & goals
│   ├── ROADMAP.md      # Features & milestones
│   └── STATE.md        # Memory: decisions, blockers, lessons, todos, deferred ideas
├── codebase/           # Brownfield analysis (existing projects)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   ├── INTEGRATIONS.md
│   └── CONCERNS.md
├── features/
│   └── [feature]/
│       ├── spec.md     # ← this skill
│       ├── context.md  # ← this skill (when gray areas exist)
│       ├── design.md   # /spec:design
│       └── tasks.md    # /spec:run
└── quick/
    └── NNN-slug/
        ├── TASK.md
        └── SUMMARY.md
```

## Commands

**Project-level:**
| Trigger Pattern | Reference |
|----------------|-----------|
| Initialize project, setup project | [project-init.md](references/project-init.md) |
| Create roadmap, plan features | [roadmap.md](references/roadmap.md) |
| Map codebase, analyze existing code | [brownfield-mapping.md](references/brownfield-mapping.md) |
| Document concerns, find tech debt, what's risky | [concerns.md](references/concerns.md) |
| Record decision, log blocker, add todo | [state-management.md](references/state-management.md) |
| Pause work, end session | [session-handoff.md](references/session-handoff.md) |
| Resume work, continue | [session-handoff.md](references/session-handoff.md) |

**Feature-level:**
| Trigger Pattern | Reference |
|----------------|-----------|
| Specify feature, define requirements | [specify.md](references/specify.md) |
| Discuss feature, how should this work, capture context | [discuss.md](references/discuss.md) |

## Discuss: When to Trigger

- The spec contains user-facing behavior that could go multiple ways AND the user hasn't expressed a preference
- Layout preferences, interaction patterns, error handling style, content tone
- **NOT for:** infrastructure, CRUD, well-defined API contracts, anything where the "how" is obvious from the "what"

## Context Loading

**Base load (~15k tokens):**
- PROJECT.md (if exists)
- ROADMAP.md (when planning/working on features)
- STATE.md (persistent memory)

**On-demand:**
- Codebase docs (when working in existing project)
- CONCERNS.md (when planning features that touch flagged areas)

**Target:** <40k tokens | **Reserve:** 160k+ for work

## Knowledge Verification Chain

```
Step 1: Codebase → existing code, conventions, patterns
Step 2: Project docs → README, docs/, .specs/codebase/
Step 3: Context7 MCP → current API/patterns
Step 4: Web search → official docs, community patterns
Step 5: Flag as uncertain → never present as fact
```

**NEVER assume or fabricate.** Uncertainty is always preferable to fabrication.

## Skill Integrations

- **codenavi** — Check if installed for code exploration (see [code-analysis.md](references/code-analysis.md))

## On Completion

When the spec (and discuss, if needed) is complete, tell the user:

> Spec complete. Run `/compact` to free up context, then:
> - **Complex/Large features:** `/spec:design <feature>` to plan architecture
> - **Medium features:** `/spec:run <feature>` to break into tasks and implement
