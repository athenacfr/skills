# Skills Marketplace

A Claude Code plugin marketplace containing three plugin groups: `gh`, `research`, and `spec-driven`.

## Structure

```
plugins/
├── gh/                          # GitHub PR workflows
│   ├── .claude-plugin/plugin.json
│   ├── agents/code-simplifier.md
│   ├── scripts/fetch_comments.py, inspect_pr_checks.py
│   └── skills/gh:fix-ci/, gh:address-comments/, gh:open-pr/
├── research/                    # Topic & code research
│   ├── .claude-plugin/plugin.json
│   ├── agents/web-researcher.md, doc-analyst.md, repo-scout.md, repo-explorer.md
│   └── skills/research:topic/, research:code/
└── spec-driven/                 # Spec-driven development
    ├── .claude-plugin/plugin.json
    └── skills/spec:create/, spec:design/, spec:run/
```

Marketplace metadata: `.claude-plugin/marketplace.json` (root), per-plugin: `plugins/<name>/.claude-plugin/plugin.json`.

### Naming Conventions

- Skills live in `plugins/<group>/skills/<group>:<name>/SKILL.md` (colon-separated `group:name`)
- Agents live in `plugins/<group>/agents/<name>.md`
- Scripts live in `plugins/<group>/scripts/`
- Reference docs live in `skills/<group>:<name>/references/*.md`

## Skills

Each skill is a folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`, `license`, `metadata`) followed by Markdown instructions. The `description` field doubles as the trigger — it tells Claude Code when to invoke the skill.

Skills may include a `references/` subfolder with supplementary Markdown docs that get loaded as context.

### Scripting Principle

Skills are folders — they can contain scripts alongside the SKILL.md. **Prefer Python scripts for deterministic operations** (parsing, formatting, data transformation, file manipulation, JSON processing) over having the LLM do it inline. Scripts run faster, cost zero tokens, and produce consistent results. Reserve LLM reasoning for judgment calls, synthesis, and creative decisions.

Examples of what should be a script:
- Parsing GraphQL/REST responses into structured data
- Generating file paths or boilerplate from templates
- Validating JSON schemas or config files
- Transforming markdown between formats

### Writing Guidelines

- Keep SKILL.md focused on the workflow and decision-making logic
- Use `references/` for static context the LLM needs (coding principles, validation checklists)
- Trigger descriptions should be specific — list exact phrases the user might say
- Agent definitions (`agents/*.md`) should specify `tools` and `model` in frontmatter

## Scripts

- Python scripts use `gh api graphql` for GitHub data (not the REST API directly)
- Scripts are invoked via `Bash` tool from within skill workflows
- Scripts write to stdout (JSON or plain text) for the LLM to consume
- New scripts should use Python, stdlib only (no third-party imports)

## Commits

- No AI attribution in commits, PRs, or code comments
- Conventional commit style: `<type>(<scope>): <description>`
- Scope should be the plugin group name: `gh`, `research`, `spec-driven`, or `marketplace`
