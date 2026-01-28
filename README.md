# memo-agent

A Claude Code plugin that helps investment analysts create professional investment memos from dataroom documents.

## Installation

### Prerequisites

1. **Claude Code CLI** - [Install Claude Code](https://claude.ai/code) if you haven't already

2. **Python 3.9+** - Check if installed:
   ```bash
   python3 --version
   ```
   If not installed:
   - **macOS:** `brew install python`
   - **Windows:** Download from [python.org](https://www.python.org/downloads/)
   - **Linux:** `sudo apt install python3` (Ubuntu/Debian)

3. **uv** (Python package manager) - Install with:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Step 1: Install the plugin

```bash
claude plugins install cpflow/memo-agent
```

Or manually:

```bash
git clone https://github.com/cpflow/memo-agent ~/.claude/plugins/memo-agent
```

### Step 2: Install Python dependencies

```bash
uv pip install -r ~/.claude/plugins/memo-agent/requirements.txt
```

### Step 3: Restart Claude Code

Close and reopen Claude Code. The `/memo` command will now be available.

## Quick Start

### 1. Sync Your Dataroom

Use rclone or manually copy your dataroom documents to a local folder:

```bash
# Example with rclone
rclone sync dropbox:Datarooms/AcmeCorp ./dataroom/

# Or just copy/paste files into a folder
```

### 2. Create a Memo

```bash
/memo ./dataroom/
```

The plugin will:
1. Scan all documents in the folder
2. Propose which materials to include
3. Draft memo sections one at a time
4. Get your approval at each step
5. Export to Word document

## Features

- **Read multiple formats**: PDFs, Word docs, Excel spreadsheets
- **Human-in-the-loop**: Approve materials, sections, and revisions
- **Citations**: All facts traced to source documents
- **Resume support**: Pick up where you left off
- **Word export**: Professional formatting

## Usage

### Basic

```bash
/memo ./dataroom/acme-corp/
```

### With Templates

Put example memos in `templates/` to help match your firm's style:

```bash
cp ~/Documents/past-memos/*.docx templates/
/memo ./dataroom/
```

### Resuming

If you have an existing workspace, you'll be asked to resume or start fresh:

```
/memo ./dataroom/
# → "Found existing workspace. Resume where you left off?"
```

## Workflow

```
┌─────────────────┐
│  /memo [path]   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Scan Documents  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Propose         │ ◄── User: approve/adjust
│ Materials       │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Propose         │ ◄── User: approve/adjust
│ Sections        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Draft Section   │ ◄── User: approve/revise
│ (repeat)        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Export to Word  │
└─────────────────┘
```

## Memo Sections

Standard investment memo structure:

1. **Deal Summary** (400-500 words) - Transaction terms, key metrics
2. **Investment Strengths** (600-800 words) - Growth drivers, competitive moat
3. **Risk Factors** (500-700 words) - Key risks and mitigations
4. **Company Analysis** (500-700 words) - Business model, products
5. **Market Analysis** (500-700 words) - TAM, competition, trends
6. **Financial Analysis** (600-800 words) - Performance, projections
7. **Management Overview** (300-500 words) - Team backgrounds

## Project Structure

```
memo-agent/
├── commands/
│   └── memo.md              # /memo command
├── skills/
│   └── investment-memo/
│       └── SKILL.md         # Workflow orchestration
├── scripts/
│   ├── extract_pdf.py       # PDF extraction
│   ├── extract_excel.py     # Excel extraction
│   └── generate_docx.py     # Word generation
├── templates/               # Example memos (add yours)
├── output/                  # Generated files
└── requirements.txt
```

## Output

Memos are saved to:

```
output/[DealName]-Memo.docx
```

## Tips

- **Better results**: Add example memos to `templates/` to match your firm's style
- **Adjusting materials**: Say "include [filename]" or "exclude [filename]"
- **Revisions**: Give specific feedback like "make the risks section more balanced"
- **Skip sections**: Say "skip this section" to move on

## Requirements

- [Claude Code CLI](https://claude.ai/code)
- [Python 3.9+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv) (Python package manager)

## Troubleshooting

**Command `/memo` not found:**
- Make sure the plugin is installed: `claude plugins list`
- Restart Claude Code after installation

**`python3: command not found`:**
- Install Python: `brew install python` (macOS) or download from [python.org](https://www.python.org/downloads/)

**`uv: command not found`:**
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your terminal after installing

**PDF extraction errors / `ModuleNotFoundError`:**
- Reinstall dependencies: `uv pip install -r ~/.claude/plugins/memo-agent/requirements.txt`

**Permission errors:**
- Check that you have read access to the dataroom folder
