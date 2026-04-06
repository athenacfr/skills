# Athena Skills Marketplace

A single, all-in-one Claude Code plugin.

## Installation

```bash
claude plugin marketplace add athenacfr/skills
claude plugin install athena@athenacfr-skills
```

## What's Inside

### Skills (user-invokable via `/skill-name`)

| Skill | Description |
|-------|-------------|
| `gh-address-comments` | Address review comments on GitHub PRs |
| `gh-fix-ci` | Evidence-based CI failure diagnosis and fix |
| `spec` | Spec-driven development with 4 adaptive phases |
| `research` | Deep research using parallel agents |
| `code-research` | Find, clone, and explore relevant repos |

### Agents (spawned by Claude as needed)

| Agent | Description |
|-------|-------------|
| `code-simplifier` | Refines code for clarity and maintainability |
| `web-researcher` | Researches topics via web search |
| `doc-analyst` | Analyzes documentation and specs |
| `repo-scout` | Finds relevant GitHub repositories |
| `repo-explorer` | Clones and analyzes repo architecture |

### Scripts

| Script | Used by |
|--------|---------|
| `fetch_comments.py` | gh-address-comments |
| `inspect_pr_checks.py` | gh-fix-ci |

## Structure

```
plugins/athena/
├── .claude-plugin/plugin.json
├── agents/
│   ├── code-simplifier.md
│   ├── doc-analyst.md
│   ├── repo-explorer.md
│   ├── repo-scout.md
│   └── web-researcher.md
├── skills/
│   ├── code-research/SKILL.md
│   ├── gh-address-comments/SKILL.md
│   ├── gh-fix-ci/SKILL.md
│   ├── research/SKILL.md
│   └── spec/
│       ├── SKILL.md
│       └── references/ (16 files)
└── scripts/
    ├── fetch_comments.py
    └── inspect_pr_checks.py
```

## License

Individual components retain their original licenses.
