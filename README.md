# Athena Skills Marketplace

A single, all-in-one Claude Code plugin.

## Installation

```bash
claude plugin marketplace add athenacfr/skills
claude plugin install athena@athenacfr-skills
```

## What's Inside

### Skills (user-invokable via `/skill-name`)

| Skill                 | Description                                 |
| --------------------- | ------------------------------------------- |
| `gh-open-pr`          | Create a PR from the current branch         |
| `gh-address-comments` | Address review comments on GitHub PRs       |
| `gh-fix-ci`           | Evidence-based CI failure diagnosis and fix |
| `research-topic`      | Deep research using parallel agents         |
| `research-code`       | Find, clone, and explore relevant repos     |
| `spec-create`         | Define requirements and resolve gray areas  |
| `spec-design`         | Architecture and component design           |
| `spec-run`            | Break into tasks and implement              |

### Scripts

| Script                 | Plugin   | Purpose                                                       |
| ---------------------- | -------- | ------------------------------------------------------------- |
| `gather_pr_context.py` | gh       | Collects branch, commits, diff, PR template in one call       |
| `fetch_comments.py`    | gh       | Fetches all PR comments and review threads via GraphQL        |
| `inspect_pr_checks.py` | gh       | Fetches failing CI checks and extracts log snippets           |
| `search_repos.py`      | research | Searches GitHub by keyword + topic, dedupes, filters by stars |

## Structure

```
plugins/
├── gh/
│   ├── scripts/
│   └── skills/gh-open-pr/, gh-address-comments/, gh-fix-ci/
├── research/
│   ├── scripts/
│   └── skills/research-topic/, research-code/
└── spec-driven/
    └── skills/spec-create/, spec-design/, spec-run/
```

## License

Individual components retain their original licenses.
