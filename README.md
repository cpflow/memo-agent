# memo-agent

A Claude Code plugin that helps investment analysts create professional investment memos from dataroom documents.

## Getting Started (Complete Guide)

Follow these steps in order. You only need to do Steps 1-4 once.

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

### Step 3: Install uv (Python package manager)

| Platform | Command |
|----------|---------|
| **macOS/Linux** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Windows (PowerShell)** | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| **Any platform (via pip)** | `pip install uv` |

**Important:** Close and reopen your terminal after installing uv.

### Step 4: Install the memo-agent plugin

You'll need **git** installed. Check with `git --version`. If not installed:
- **macOS:** `xcode-select --install` or `brew install git`
- **Windows:** Download from [git-scm.com](https://git-scm.com/download/win)
- **Linux:** `sudo apt install git`

Clone the plugin to your Claude Code plugins directory:

**macOS/Linux:**
```bash
git clone https://github.com/cpflow/memo-agent ~/.claude/plugins/memo-agent
```

**Windows (PowerShell):**
```powershell
git clone https://github.com/cpflow/memo-agent $env:USERPROFILE\.claude\plugins\memo-agent
```

Then install the Python dependencies:

**macOS/Linux:**
```bash
uv pip install -r ~/.claude/plugins/memo-agent/requirements.txt
```

**Windows (PowerShell):**
```powershell
uv pip install -r $env:USERPROFILE\.claude\plugins\memo-agent\requirements.txt
```

### Step 5: Create your first memo

1. **Get your dataroom documents** into a local folder. You can:
   - Copy/paste files from Dropbox, email, etc.
   - Use rclone: `rclone sync dropbox:Datarooms/AcmeCorp ./my-dataroom/`
   - Just drag and drop files into a folder

2. **Open Claude Code** from any directory:
   ```bash
   claude
   ```

3. **Run the memo command** with the path to your documents:
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
- Make sure the plugin folder exists: `ls ~/.claude/plugins/memo-agent` (macOS/Linux) or `dir $env:USERPROFILE\.claude\plugins\memo-agent` (Windows)
- Restart Claude Code after installation
- Make sure the `.claude-plugin/plugin.json` file exists in the plugin folder

**`python3: command not found`:**
- Install Python: `brew install python` (macOS) or download from [python.org](https://www.python.org/downloads/)

**`uv: command not found` / `'uv' is not recognized`:**
- macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Or any platform: `pip install uv`
- Restart your terminal after installing

**PDF extraction errors / `ModuleNotFoundError`:**
- Reinstall dependencies: `uv pip install -r ~/.claude/plugins/memo-agent/requirements.txt`

**Permission errors:**
- Check that you have read access to the dataroom folder
