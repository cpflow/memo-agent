# memo-agent

A Claude Code plugin that helps investment analysts create professional investment memos from dataroom documents.

## Getting Started (Complete Guide)

Follow these steps in order. You only need to do Steps 1-3 once (setup).

### Step 1: Install Claude Code

If you don't have Claude Code installed, get it from [claude.ai/code](https://claude.ai/code).

Verify it's working by opening a terminal and running:
```bash
claude --version
```

### Step 2: Install Python

Check if Python is already installed:
```bash
python3 --version
```

If you see `command not found` or a version below 3.9, install Python:

| Platform | Command |
|----------|---------|
| **macOS** | `brew install python` |
| **Windows** | Download from [python.org](https://www.python.org/downloads/) and run the installer. **Check "Add Python to PATH"** during installation. |
| **Linux (Ubuntu/Debian)** | `sudo apt install python3` |

### Step 3: Install the memo-agent plugin

First, install the Python dependencies (run this in your terminal):

```bash
pip install pdfplumber python-docx openpyxl
```

Then open Claude Code and run these commands:

```
/plugin marketplace add cpflow/memo-agent
/plugin install memo-agent@cpflow-memo-agent
```

### Step 4: Create your first memo

1. **Get your dataroom documents** into a local folder. You can:
   - Copy/paste files from Dropbox, email, etc.
   - Use rclone: `rclone sync dropbox:Datarooms/AcmeCorp ./my-dataroom/`
   - Just drag and drop files into a folder

2. **Run the memo command** in Claude Code with the path to your documents:
   ```
   /memo ./my-dataroom/
   ```

4. **Follow the prompts.** The plugin will:
   - Scan all documents in the folder
   - Ask you to approve which materials to use
   - Draft each memo section one at a time
   - Ask for your approval before moving to the next section
   - Export to a Word document when complete

## Features

- **Read multiple formats**: PDFs, Word docs, Excel spreadsheets
- **Human-in-the-loop**: Approve materials, sections, and revisions
- **Citations**: All facts traced to source documents
- **Resume support**: Pick up where you left off
- **Word export**: Professional formatting

## Usage

### Basic

```
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
┌─────────────────────────┐
│  /memo [path]│
└───────────┬─────────────┘
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
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace config
├── commands/
│   └── memo.md              # /memo command
├── skills/
│   └── investment-memo/
│       ├── SKILL.md         # Workflow orchestration
│       └── scripts/         # Extraction scripts (per Claude Code best practices)
│           ├── extract_pdf.py
│           ├── extract_excel.py
│           └── generate_docx.py
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

## Troubleshooting

**Command `/memo` not found:**
- Make sure you installed the plugin:
  ```
  /plugin marketplace add cpflow/memo-agent
  /plugin install memo-agent@cpflow-memo-agent
  ```
- Run `/plugin` and check the **Installed** tab to verify the plugin is installed
- Try restarting Claude Code after installation

**`python3: command not found`:**
- Install Python: `brew install python` (macOS) or download from [python.org](https://www.python.org/downloads/)

**PDF extraction errors / `ModuleNotFoundError`:**
- Install the dependencies: `pip install pdfplumber python-docx openpyxl`

**Permission errors:**
- Check that you have read access to the dataroom folder

## Updating

To update the plugin to the latest version:

```
/plugin marketplace update cpflow-memo-agent
/plugin update memo-agent@cpflow-memo-agent
```
