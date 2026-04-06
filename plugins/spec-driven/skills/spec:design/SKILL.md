---
name: spec:design
description: Define architecture, components, interfaces, and data models for a feature. Identifies code reuse, integration points, and error handling. Produces design.md. Use when user says "design feature", "architecture", or for Large/Complex features that need architectural planning. Skip for straightforward changes with no new patterns. Do NOT use for requirements (use /spec:create) or implementation (use /spec:run). After completing, recommend user runs /compact then /spec:run <feature>.
license: MIT
metadata:
  author: Athena Freitas - github.com/athenacfr
  version: 1.0.0
---

# Spec: Design

**Usage:** `/spec:design <feature>`

Define HOW to build a feature. Architecture, components, what to reuse. Produces `.specs/features/<feature>/design.md`.

## When to Use

- Large features (multi-component, many integration points)
- Complex features (ambiguity, new domain, unfamiliar tech)
- NOT for: straightforward changes, no new patterns, no architectural decisions

## Process

See [design.md](references/design.md) for the full workflow.

1. **Load Context** — Read `spec.md` and `context.md` (if exists from `/spec:create`)
2. **Research** — Follow Knowledge Verification Chain for unfamiliar tech/patterns
3. **Architecture** — Define component interactions, use mermaid diagrams
4. **Code Reuse** — Identify existing components to leverage (check CONCERNS.md if it exists)
5. **Components** — Define each: purpose, location, interfaces, dependencies
6. **Data Models** — Define schemas and relationships
7. **Error Handling** — Strategy per error scenario
8. **Tech Decisions** — Document non-obvious choices with rationale

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

- **mermaid-studio** — Check if installed before creating diagrams
- **codenavi** — Check if installed for code exploration (see [code-analysis.md](references/code-analysis.md))

## On Completion

When the design is complete, tell the user:

> Design complete. Run `/compact` to free up context, then `/spec:run <feature>` to break into tasks and implement.
