---
title: "Claude Code Plugin Development: Script Paths, Encoding, and Installation"
category: configuration-fixes
tags:
  - claude-code
  - plugin-development
  - skills
  - python
  - utf-8-encoding
  - excel
  - windows
  - script-resolution
  - marketplace
module: Claude Code Plugin
symptom: |
  Multiple errors when developing Claude Code plugins:
  - Plugin not found after git clone
  - Scripts fail with "file not found" when skill invoked
  - UnicodeEncodeError on Windows when printing non-ASCII characters
  - Unhandled exceptions when Excel files are missing or malformed
root_cause: |
  1. Plugins require marketplace distribution or proper local installation
  2. Script paths in SKILL.md must use full paths from plugin root
  3. Windows console defaults to cp1252 encoding, causing crashes with UTF-8 content
  4. Missing validation for file existence and format before processing
---

# Claude Code Plugin Development: Script Paths, Encoding, and Installation

## Problem Summary

When developing a Claude Code plugin with Python scripts, multiple configuration issues can cause failures:
- Plugin not discovered after installation
- Scripts not found when skill is invoked
- Unicode encoding errors on Windows
- Unhandled exceptions for file operations

## Solution

### 1. Plugin Structure

Plugins need specific structure for marketplace distribution:

**Directory structure:**
```
my-plugin/
├── .claude-plugin/
│   ├── marketplace.json    # Required for plugin discovery
│   └── plugin.json         # Minimal plugin metadata
├── skills/
│   └── my-skill/
│       ├── SKILL.md        # Skill instructions
│       └── scripts/        # Support scripts HERE
│           └── my_script.py
└── commands/
    └── my-command.md       # Slash commands (auto-discovered)
```

**`.claude-plugin/marketplace.json`** - Note `"source": "./"` not `"."`
```json
{
  "name": "owner-plugin-name",
  "owner": {
    "name": "owner"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./",
      "description": "Plugin description",
      "version": "0.1.0"
    }
  ]
}
```

**`.claude-plugin/plugin.json`** - Keep minimal; commands/skills are auto-discovered
```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Plugin description"
}
```

### 2. Script Path Resolution in SKILL.md

Paths in SKILL.md resolve from the **plugin root**, not the skill directory. The `${CLAUDE_PLUGIN_ROOT}` variable only works in hooks and MCP configs, not in SKILL.md content.

```markdown
<!-- WRONG - paths don't resolve from skill directory -->
python scripts/extract_pdf.py "<file>"

<!-- WRONG - variable not expanded in SKILL.md -->
python ${CLAUDE_PLUGIN_ROOT}/skills/my-skill/scripts/script.py "<file>"

<!-- CORRECT - full path from plugin root -->
python skills/investment-memo/scripts/extract_pdf.py "<file>" 1 10
```

### 3. Windows Encoding Fix

`sys.stdout = io.TextIOWrapper(...)` doesn't work reliably on Windows cp1252. Use:

```python
#!/usr/bin/env python3
import sys
import os

# Fix Windows encoding - set BEFORE any output
os.environ["PYTHONIOENCODING"] = "utf-8"

def safe_print(text):
    """Print text safely, replacing unencodable characters."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))

# Usage: safe_print(result) instead of print(result)
```

### 4. Excel Extraction Robustness

```python
from pathlib import Path
from openpyxl import load_workbook

def extract(path: str, max_rows: int = 50) -> str:
    file_path = Path(path)

    # Check 1: File exists
    if not file_path.exists():
        return f"[Error: File not found: {path}]"

    # Check 2: Supported format
    ext = file_path.suffix.lower()
    if ext == '.xls':
        return f"[Error: Old .xls format not supported. Convert to .xlsx]"

    if ext not in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
        return f"[Error: Unsupported format: {ext}]"

    # Check 3: Handle protected/corrupted files
    try:
        wb = load_workbook(path, read_only=True, data_only=True)
    except Exception as e:
        error_msg = str(e)
        if "password" in error_msg.lower():
            return f"[Error: File is password-protected: {path}]"
        return f"[Error opening file: {error_msg}]"

    # Process workbook...
```

## Prevention Checklist

### Plugin Structure
- [ ] Use `"source": "./"` in marketplace.json (not `"."`)
- [ ] Keep plugin.json minimal - let auto-discovery work
- [ ] Place scripts in `skills/<name>/scripts/` directory

### Script Paths
- [ ] Use full paths from plugin root: `skills/skill-name/scripts/script.py`
- [ ] Don't rely on `${CLAUDE_PLUGIN_ROOT}` in SKILL.md
- [ ] Test with fresh plugin installation

### Encoding
- [ ] Set `os.environ["PYTHONIOENCODING"] = "utf-8"` at module level
- [ ] Use `safe_print()` wrapper for all output
- [ ] Test with files containing Unicode characters

### Error Handling
- [ ] Validate file exists before opening
- [ ] Check file format/extension
- [ ] Wrap file operations in try/except
- [ ] Return error strings, don't raise exceptions

## Related

- [Claude Code Plugin Documentation](https://code.claude.com/docs/en/plugins-reference.md)
- [Skills Documentation](https://code.claude.com/docs/en/skills.md)
