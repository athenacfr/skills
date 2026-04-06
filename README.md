# Athena Skills Marketplace

A curated collection of Claude Code skills and plugins.

## Installation

Install skills directly from this marketplace:

```bash
/plugin install <plugin-name>@athenacfr/skills
```

Or browse available plugins:

```bash
/plugin > Discover
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `code-simplifier` | Simplifies and refines code for clarity, consistency, and maintainability |
| `gh-address-comments` | Address review comments on GitHub PRs using gh CLI |
| `gh-fix-ci` | Debug and fix failing GitHub Actions PR checks |
| `tlc-spec-driven` | Spec-driven development with 4 adaptive phases |

## Plugin Structure

Each plugin follows the standard Claude Code plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (required)
├── skills/              # Skill definitions (optional)
│   └── skill-name/
│       ├── SKILL.md     # Main skill definition
│       └── references/  # Supporting docs (optional)
├── agents/              # Agent definitions (optional)
├── commands/            # Slash commands (optional)
├── scripts/             # Helper scripts (optional)
└── LICENSE
```

## Contributing

Submit a PR to add a new plugin. Follow the structure above and include a LICENSE.

## License

Individual plugins retain their own licenses. See each plugin directory.
