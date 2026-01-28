---
title: "Claude Code Plugin Installation and Distribution"
category: plugin-development
tags: [claude-code, plugin, installation, plugin-dir, marketplace, cross-platform]
module: Plugin System
symptom: "Users unable to install Claude Code plugins, confusion about installation process"
root_cause: "Official method uses --plugin-dir flag for local plugins, not manual file placement"
created: 2026-01-28
---

## Problem

When building a Claude Code plugin for distribution, there was confusion about the installation process. Initial attempts included:
1. Cloning directly to `~/.claude/plugins/[name]` (doesn't work)
2. Manually editing `installed_plugins.json` (internal format, not official)

## Solution

The official Claude Code documentation provides two methods:

### Method 1: Local Development/Testing (--plugin-dir flag)

For plugins that aren't in a marketplace, use the `--plugin-dir` flag:

```bash
# Clone the plugin anywhere
git clone https://github.com/[org]/[repo] ~/my-plugin

# Start Claude Code with the plugin loaded
claude --plugin-dir ~/my-plugin
```

**Key points:**
- Plugin can be cloned to any location
- Must use `--plugin-dir` flag each time you start Claude Code
- Commands are namespaced: `/plugin-name:command`
- Multiple plugins can be loaded: `claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two`

**Shell alias for convenience:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias claude-memo='claude --plugin-dir ~/memo-agent'
```

### Method 2: Marketplace Distribution (for sharing)

For permanent installation, plugins should be distributed via a marketplace:

1. Create a plugin marketplace (GitHub repo with plugin releases)
2. Users add the marketplace: `/plugin marketplace add your-org/plugins`
3. Users install: `/plugin install plugin-name@marketplace`

See [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) for details.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Required manifest (ONLY file in this directory)
├── commands/             # Slash commands (at root, NOT inside .claude-plugin)
├── skills/               # Agent skills
├── agents/               # Custom agents
├── hooks/                # Event handlers
└── scripts/              # Helper scripts
```

**Common mistake:** Don't put `commands/`, `skills/`, etc. inside `.claude-plugin/`. Only `plugin.json` goes there.

## Key Insights

1. **No built-in local install command**: `claude plugins install` doesn't exist for local plugins
2. **--plugin-dir is the official method**: For local/development plugins
3. **Commands are namespaced**: `/plugin-name:command`, not just `/command`
4. **Marketplaces for distribution**: For permanent installation by others
5. **Shell aliases help**: Avoid typing `--plugin-dir` every time

## References

- [Official plugins documentation](https://code.claude.com/docs/en/plugins)
- [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
