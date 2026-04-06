---
name: gh:open-pr
description: Create a GitHub pull request from the current branch. Use when user says "open PR", "create PR", "submit PR", "make a pull request", or "push and open PR". Gathers commit history, drafts a title and description, and opens the PR via gh CLI. Do NOT use for addressing PR comments (use /gh:address-comments) or fixing CI (use /gh:fix-ci).
license: MIT
metadata:
  author: Athena - github.com/athenacfr/skills
  version: 1.0.0
---

# Open Pull Request

Create a well-structured GitHub PR from the current branch using `gh` CLI.

## Prerequisites

Ensure `gh` is authenticated: `gh auth status` (repo scope required).
If not authenticated, instruct the user to run `gh auth login`.

## Workflow

### Phase 1: Gather Context

Run these in parallel:

1. **Current branch & remote status**
   ```
   git branch --show-current
   git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
   ```

2. **Detect base branch** — use the repo default:
   ```
   gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
   ```

3. **Commit history since divergence from base**
   ```
   git log --oneline <base>..HEAD
   git diff <base>...HEAD --stat
   ```

4. **Check for uncommitted changes**
   ```
   git status --short
   ```

5. **Check for PR template** (MANDATORY)
   ```
   Look for .github/pull_request_template.md, .github/PULL_REQUEST_TEMPLATE.md,
   or .github/PULL_REQUEST_TEMPLATE/ directory
   ```

### Phase 2: Prepare

1. If there are uncommitted changes, ask the user if they want to commit first
2. If the branch has no upstream, note that `gh pr create` will push automatically
3. Analyze the commit history and diff to draft:
   - **Title**: conventional commit style `<type>(<scope>): <description>` (under 70 chars)
   - **Body**: **ALWAYS** follow the repo's `.github/pull_request_template.md` if it exists. Read the template, fill in every section with relevant content from the commits and diff. Do NOT skip sections — if a section is not applicable, explicitly mark it as N/A. Only use the fallback format below if no PR template exists in the repo.

Fallback body format (only when no PR template exists):
```
## Context
[Why this change exists — explain the motivation/problem BEFORE describing the solution]

## Changes
[Grouped by purpose/area, NOT by file. Bullet points.]

## Feature Flags
[Only include this section if feature flags were actually added. Otherwise omit entirely.]

## Breaking Changes
[Only include if there are breaking changes. Highlight prominently.]
```

### Phase 3: Confirm & Create

1. Present the draft title and body to the user
2. Ask for approval or edits
3. Once confirmed, create the PR:
   ```
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   <body>
   EOF
   )"
   ```
   - Add `--base <branch>` if targeting a non-default branch
   - Add `--draft` if the user requests a draft PR
   - Add `--label`, `--reviewer`, `--assignee` flags if the user specifies them

4. Output the PR URL

## Anti-Patterns (DO NOT)

- **DO NOT** create the PR without showing the draft to the user first
- **DO NOT** add AI attribution or "Co-Authored-By" lines
- **DO NOT** push force or rebase without explicit user request
- **DO NOT** list files individually in the PR body — group changes by purpose
- **DO NOT** include changes from the base branch in the description — only describe what this branch adds
