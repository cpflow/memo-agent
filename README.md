# memo-agent

A Claude Code plugin that helps investment analysts create professional investment memos from dataroom documents.

## Installation

### Option 1: Install via Claude Code CLI (recommended)

```bash
claude plugins install cpflow/memo-agent
```

Then install Python dependencies:

```bash
pip install -r ~/.claude/plugins/memo-agent/requirements.txt
```

### Option 2: Manual installation

```bash
# Clone the repository
git clone https://github.com/cpflow/memo-agent ~/.claude/plugins/memo-agent

# Install Python dependencies
pip install -r ~/.claude/plugins/memo-agent/requirements.txt
```

After installation, restart Claude Code. The `/memo` command will be available.

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

- [Claude Code CLI](https://claude.ai/code) installed and configured
- Python 3.9+
- Python packages (installed automatically): `pdfplumber`, `python-docx`, `openpyxl`

## Troubleshooting

**Command `/memo` not found:**
- Make sure the plugin is installed: `claude plugins list`
- Restart Claude Code after installation

**PDF extraction errors:**
- Run `pip install pdfplumber` to ensure dependencies are installed

**Permission errors:**
- Check that you have read access to the dataroom folder
