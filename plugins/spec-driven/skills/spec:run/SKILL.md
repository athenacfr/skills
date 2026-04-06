---
name: spec:run
description: Break specs into tasks and execute them. Creates atomic task breakdowns, implements ONE task at a time with verification, gate checks, and atomic git commits. Use when (1) Breaking features into tasks, (2) Implementing tasks from a spec (after /spec planning), (3) Quick ad-hoc tasks (bug fixes, config changes), (4) Validating and verifying work, (5) Running UAT walkthroughs. Triggers on "break into tasks", "create tasks", "implement", "execute", "build", "validate", "verify work", "UAT", "walk me through it", "quick fix", "quick task", "small change", "bug fix". Do NOT use for specifying requirements (use /spec:create) or architecture (use /spec:design).
license: MIT
metadata:
  author: Athena - github.com/athenacfr/skills
  version: 1.0.0
---

# Spec: Run

Break specs into tasks and execute them. One task at a time. Verify. Commit. Repeat.

**Usage:** `/spec:run <feature>`

The argument is the feature name from `.specs/features/<feature>/`. The skill loads the spec, breaks it into tasks (if not already done), and implements them.

```
┌─────────┐   ┌─────────┐   ┌──────────┐   ┌──────────┐
│  TASKS  │ → │IMPLEMENT│ → │  VERIFY  │ → │  COMMIT  │   (repeat per task)
└─────────┘   └─────────┘   └──────────┘   └──────────┘
  once          per task      per task       per task
```

Use `/spec:create` first to define requirements, then `/spec:run <feature>` to break into tasks and build.

## Quick Mode

For small tasks (≤3 files, one-sentence scope): Describe → Implement → Verify → Commit. See [quick-mode.md](references/quick-mode.md).

## Project Structure

```
.specs/
├── project/
│   ├── PROJECT.md      # Vision & goals
│   ├── ROADMAP.md      # Features & milestones
│   └── STATE.md        # Memory: decisions, blockers, lessons, todos, deferred ideas
├── codebase/           # Brownfield analysis (existing projects)
│   └── TESTING.md      # Test patterns and gate check commands
├── features/           # Feature specifications
│   └── [feature]/
│       ├── spec.md     # Requirements with traceable IDs
│       ├── design.md   # Architecture & components
│       └── tasks.md    # Atomic tasks with verification
└── quick/              # Ad-hoc tasks (quick mode)
    └── NNN-slug/
        ├── TASK.md
        └── SUMMARY.md
```

## Context Loading

- STATE.md (persistent memory)
- TESTING.md (gate check commands and test patterns)
- spec.md (current feature requirements)
- design.md (current feature architecture)
- tasks.md (current feature task breakdown)
- [coding-principles.md](references/coding-principles.md) (always)

## Sub-Agent Delegation

Use sub-agents to keep the main context window lean and enable parallel execution.

| Activity | Delegate? | Why |
|---|---|---|
| Implementing a task | Yes | File reads, edits, test output consume context; only the result matters |
| Parallel `[P]` tasks | Yes (one per task) | The only way to actually run tasks in parallel |
| Sequential tasks with no `[P]` | Yes | Keeps implementation artifacts out of the main context |
| Validation reports | No | These require the full accumulated context to be coherent |
| Quick mode tasks | No | Too small to justify the overhead |

**Context each sub-agent receives:**

The orchestrating agent MUST provide each sub-agent with:
- The specific task definition from tasks.md (What, Where, Depends on, Reuses, Done when, Tests, Gate)
- Relevant coding principles and conventions (coding-principles.md, CONVENTIONS.md)
- TESTING.md, if it exists (for gate check commands and test patterns)
- Any spec/design context the task references

The sub-agent does NOT receive: other tasks' definitions, accumulated chat history, validation reports from other tasks, or STATE.md (unless the task explicitly references a decision/blocker).

**What sub-agents return:**

Each sub-agent reports back:
- Status: Complete | Blocked | Partial
- Files changed: [list]
- Gate check result: [pass/fail + test counts]
- SPEC_DEVIATION markers (if any)
- Issues encountered (if any)

The orchestrating agent uses this to update tasks.md status, traceability, and decide next steps.

## Workflow

### Phase 1: Load Spec

Load `.specs/features/<spec-name>/spec.md` (and `design.md` if it exists). If the spec doesn't exist, tell the user to run `/spec` first.

### Phase 2: Break Into Tasks

If `.specs/features/<spec-name>/tasks.md` doesn't exist yet, create it. See [tasks.md](references/tasks.md) for the full task breakdown format.

### Phase 3: Implement

## Commands

| Trigger Pattern | Reference |
|----------------|-----------|
| Break into tasks, create tasks | [tasks.md](references/tasks.md) |
| Implement task, build, execute | [implement.md](references/implement.md) |
| Validate, verify, test, UAT, walk me through it | [validate.md](references/validate.md) |
| Quick fix, quick task, small change, bug fix | [quick-mode.md](references/quick-mode.md) |

## Implementation Process

See [implement.md](references/implement.md) for the full process. Summary:

### 0. List Atomic Steps (when no tasks.md exists)

If there is no `tasks.md`, list atomic steps before writing code. If >5 steps emerge, create a formal `tasks.md`.

### 1-2. Pick Task & Verify Dependencies

From tasks.md or execution plan. Check dependencies before starting.

### 3. State Implementation Plan

```
Files: [list]
Approach: [brief description]
Success: [how to verify]
```

### 4. Write Tests First (RED) → 4b. Implement (GREEN)

Tests define the spec. Implementation conforms to tests. Never modify tests to pass.

### 5. Gate Check (VERIFY)

Run the gate check command. Non-zero exit = STOP and fix.

| Task includes                    | Gate level | What runs                |
| -------------------------------- | ---------- | ------------------------ |
| Unit tests only                  | Quick      | Unit test command        |
| E2E or integration tests         | Full       | Unit + E2E commands      |
| Last task in a phase             | Build      | Build + lint + all tests |
| No tests (config, entities, etc) | Build      | Build + lint only        |

### 6-7. Post-Gate Review → Atomic Git Commit

One task = one commit. Conventional Commits format. No "while I'm here" changes.

### 8-9. Scope Guardrail → Update Task Status

If it's not in the task definition, don't touch it. Log improvements in STATE.md.

## Knowledge Verification Chain

When making any technical decision, follow this chain in strict order:

```
Step 1: Codebase → check existing code, conventions, and patterns already in use
Step 2: Project docs → README, docs/, inline comments, .specs/codebase/
Step 3: Context7 MCP → resolve library ID, then query for current API/patterns
Step 4: Web search → official docs, reputable sources, community patterns
Step 5: Flag as uncertain → "I'm not certain about X — here's my reasoning, but verify"
```

**NEVER assume or fabricate.** Uncertainty is always preferable to fabrication.
