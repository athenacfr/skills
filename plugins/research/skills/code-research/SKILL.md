---
name: code-research
description: Code-focused research that finds, clones, and explores relevant repositories. Use when user says "find repos for", "how do others implement", "code research", "find examples of", "explore how [project] works", "clone and analyze", or asks about implementation patterns, library comparisons, or codebase architecture. Do NOT use for general topic research (use research instead).
license: MIT
metadata:
  author: Athena - github.com/athenacfr/skills
  version: 1.0.0
---

# Code Research

Find, clone, and explore relevant repositories to understand implementation patterns, architectures, and real-world code.

## How It Works

This skill runs in two phases:
1. **Scout phase** — parallel agents search for relevant repos
2. **Explore phase** — parallel agents clone and deeply analyze the best finds

## Workflow

### 1. Understand the Research Goal

Parse the user's request and identify:
- **What to find** — libraries, frameworks, implementations, patterns
- **Why** — comparing options, learning patterns, finding reference implementations
- **Constraints** — language, framework, license, activity level preferences

### 2. Phase 1: Scout (Parallel)

Launch **2-3 agents in parallel** to find relevant repositories from different angles:

| Agent | Focus |
|-------|-------|
| Agent 1 | Direct search — repos matching the core query |
| Agent 2 | Ecosystem search — related tools, alternatives, awesome-lists |
| Agent 3 | Implementation examples — real-world usage, starter templates |

**Each scout agent prompt MUST include:**
- The specific search angle
- Instruction to use WebSearch to find GitHub repos
- Instruction to evaluate quality (stars, recent activity, docs)
- Instruction to return a ranked list with URLs and reasons

**Example scout prompt:**
```
Search the web for GitHub repositories related to: [specific angle]

For each repo found, note:
- Full URL (https://github.com/owner/repo)
- Star count and last commit date if visible
- Why it's relevant
- Language/framework

Return your top 3-5 picks ranked by relevance. Be specific about WHY each is worth exploring.
```

### 3. Evaluate & Select

After scouts return:
- Deduplicate repos found across agents
- Rank by relevance to the user's goal
- **Select 1-3 repos** for deep exploration (ask user if unclear which to prioritize)

Present a quick summary:
```
Found [N] relevant repos. Top picks for deep dive:
1. **owner/repo** — [why]
2. **owner/repo** — [why]
3. **owner/repo** — [why]

Cloning and exploring these now...
```

### 4. Phase 2: Explore (Parallel)

Launch **parallel agents** (one per selected repo) to clone and analyze:

**Each explorer agent prompt MUST include:**
- The repo URL to clone
- Instruction to clone with `git clone --depth 1` to `/tmp/research-repos/[owner]-[repo]`
- The specific aspects to investigate (architecture, patterns, how they handle X)
- Instruction to read key files: README, entry points, config, core modules

**Example explorer prompt:**
```
Clone and analyze this repository: https://github.com/owner/repo

1. Clone: `git clone --depth 1 https://github.com/owner/repo /tmp/research-repos/owner-repo`
2. Map the directory structure (tree, depth 3)
3. Identify the stack (check package.json, Cargo.toml, go.mod, etc.)
4. Read the README and key entry points
5. Find how they handle: [specific aspect user cares about]
6. Note interesting architectural patterns

Return a structured analysis:
- Purpose and stack
- Directory layout (annotated)
- Architecture pattern
- Key files and their roles
- Notable patterns or techniques
- The clone path for further exploration

Keep under 600 words. Focus on architecture and patterns, not line-by-line code.
```

### 5. Synthesize & Report

Combine all explorer findings:

```markdown
## Code Research: [topic]

### Summary
[What was found and the key takeaway]

### Repositories Analyzed

#### 1. owner/repo
- **URL**: https://github.com/owner/repo
- **Stack**: [languages, frameworks]
- **Architecture**: [pattern description]
- **Key insight**: [most valuable finding]
- **Cloned to**: `/tmp/research-repos/owner-repo`

#### 2. owner/repo
...

### Pattern Comparison
| Aspect | repo-1 | repo-2 | repo-3 |
|--------|--------|--------|--------|
| Architecture | ... | ... | ... |
| State mgmt | ... | ... | ... |
| Testing | ... | ... | ... |

### Recommendations
[Which approach fits the user's needs and why]

### Cloned Repos
All repos are available locally for further exploration:
- `/tmp/research-repos/owner-repo1`
- `/tmp/research-repos/owner-repo2`
```

### 6. Offer Next Steps

- "Want me to read specific files in any of these repos?"
- "Should I extract [specific pattern] from [repo] into your project?"
- "Want a deeper comparison of [aspect]?"

## Guidelines

- **Two-phase approach** — always scout first, then explore. Don't clone blindly
- **Parallel everything** — scouts run in parallel, explorers run in parallel
- **Shallow clones** — always `--depth 1` to save time and space
- **Clone to `/tmp/research-repos/`** — consistent location, easy cleanup
- **Ask before exploring more than 3 repos** — each clone costs time
- **Focus on architecture** — the user wants patterns and structure, not to read every line
- **Compare when possible** — side-by-side comparisons are more valuable than isolated summaries
- **Leave repos cloned** — the user may want to explore further after the report
