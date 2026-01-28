---
title: "Claude Code Plugin Installation and Distribution"
category: plugin-development
tags: [claude-code, plugin, installation, marketplace, distribution]
module: Plugin System
symptom: "Users unable to install Claude Code plugins, confusion about installation process"
root_cause: "Plugins must be distributed via a marketplace for proper installation"
created: 2026-01-28
---

## Problem

When building a Claude Code plugin for distribution, there was confusion about the installation process. Initial incorrect attempts included:
1. Cloning directly to `~/.claude/plugins/[name]` (doesn't work)
2. Manually editing `installed_plugins.json` (internal format, not official)
3. Using `--plugin-dir` flag (development/testing only, not for distribution)

## Solution

The official method for distributing plugins is via a **marketplace**. A single plugin repo can be its own marketplace.

### Step 1: Add marketplace.json to your plugin

Create `.claude-plugin/marketplace.json` alongside your existing `plugin.json`:

```json
{
  "name": "your-org-plugin-name",
  "owner": {
    "name": "Your Name or Org"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./",
      "description": "Your plugin description",
      "version": "1.0.0"
    }
  ]
}
```

**Important:** Use `"./"` not `"."` for the source path.

Key points:
- `name` in marketplace.json becomes the marketplace identifier (e.g., `cpflow-memo-agent`)
- `source: "."` points to the current repo (the plugin itself)
- The plugin `name` is what users reference when installing

### Step 2: User installation

Users install with two commands:

```
/plugin marketplace add your-org/your-repo
/plugin install plugin-name@marketplace-name
```

Example:
```
/plugin marketplace add cpflow/memo-agent
/plugin install memo-agent@cpflow-memo-agent
```

### Plugin manifest (plugin.json)

Keep it minimal - commands and skills in default directories are auto-discovered:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Your plugin description"
}
```

**Do NOT use object format for commands/skills** - this is invalid:
```json
// WRONG - causes "Invalid input" error
{
  "commands": { "memo": "./commands/memo.md" },
  "skills": { "my-skill": "./skills/my-skill" }
}
```

### Directory Structure

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json       # Plugin manifest (required)
│   └── marketplace.json  # Marketplace manifest (required for distribution)
├── commands/             # Slash commands (auto-discovered)
├── skills/               # Agent skills (auto-discovered)
├── agents/               # Custom agents (auto-discovered)
└── scripts/              # Helper scripts
```

## Key Insights

1. **Marketplaces are required for distribution**: The `/plugin install` command only works with marketplaces
2. **A plugin repo can be its own marketplace**: Add `marketplace.json` with `"source": "./"`
3. **Use "./" not "."**: The source path must be `"./"` not `"."` (causes "invalid schema" error)
4. **Keep plugin.json minimal**: Don't specify commands/skills as objects - they're auto-discovered from directories
5. **Commands are namespaced**: `/plugin-name:command`, not just `/command`
6. **--plugin-dir is for development only**: Not for end-user installation
7. **No manual file placement**: Don't tell users to clone to `~/.claude/plugins/`

## Alternative: Development/Testing Only

For local development, use `--plugin-dir`:

```bash
claude --plugin-dir ./my-plugin
```

This is NOT for distribution - only for testing during development.

## References

- [Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)
- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- [Create plugins](https://code.claude.com/docs/en/plugins)
