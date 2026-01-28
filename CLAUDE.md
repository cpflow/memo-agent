# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**memo-agent** is a Claude Code plugin that helps investment analysts create professional investment memos from dataroom documents.

## Build & Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test PDF extraction
python scripts/extract_pdf.py path/to/file.pdf

# Test Excel extraction
python scripts/extract_excel.py path/to/file.xlsx

# Test Word generation
python scripts/generate_docx.py input.md output.docx
```

## Architecture

```
memo-agent/
├── commands/
│   └── memo.md              # /memo command entry point
├── skills/
│   └── investment-memo/
│       └── SKILL.md         # Main workflow orchestration
├── scripts/
│   ├── extract_pdf.py       # PDF text/table extraction (pdfplumber)
│   ├── extract_excel.py     # Excel extraction (openpyxl)
│   └── generate_docx.py     # Markdown to Word conversion (python-docx)
├── templates/               # Example memos for style matching
├── output/                  # Generated memo files
├── requirements.txt         # Python dependencies
└── docs/plans/              # Planning documents
```

## Key Patterns

### Document Extraction
- PDFs: `python scripts/extract_pdf.py <file>` - outputs text with page markers and tables
- Excel: `python scripts/extract_excel.py <file>` - outputs markdown tables
- Word/Text: Use Read tool directly

### Workspace
Progress is saved to `.memo-workspace/`:
- `status.txt` - current step and completed sections
- `memo.md` - the draft memo being built
- `materials.txt` - included/excluded files

### Workflow
1. Scan documents in folder
2. Propose materials → get approval
3. Propose sections → get approval
4. Draft each section → get approval
5. Export to Word

## Usage

```
/memo ./dataroom/acme-corp/
```

## Dependencies

- `pdfplumber` - PDF text and table extraction
- `python-docx` - Word document generation
- `openpyxl` - Excel file reading
