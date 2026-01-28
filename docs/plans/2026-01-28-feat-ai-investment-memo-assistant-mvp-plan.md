---
title: AI Investment Memo Writing Assistant - MVP
type: feat
date: 2026-01-28
version: mvp
---

# AI Investment Memo Writing Assistant - MVP

## Overview

A Claude Code plugin that helps investment analysts create investment memos by reading dataroom documents and drafting sections with human approval at each step.

**Core loop:** Read documents → Draft sections → Get approval → Export Word doc

## What This MVP Does

1. Reads documents from a local folder (synced from Dropbox via rclone)
2. Proposes which documents are relevant for the memo
3. Drafts memo sections one at a time with human approval
4. Exports to Word document

## What This MVP Does NOT Do (Deferred to v2+)

- ~~State machine with validated transitions~~ → Simple step tracker
- ~~13 MCP checkpoint tools~~ → Natural conversation
- ~~MNPI protocol / secure deletion~~ → Trust the user
- ~~Hash-chained audit logs~~ → Simple text log
- ~~Style Guardian agent~~ → Style guide in prompts
- ~~Learning/compounding system~~ → Templates folder
- ~~Central sync~~ → Local only
- ~~Parallel document processing~~ → Sequential is fine
- ~~Hierarchical summarization~~ → Truncate with warning
- ~~Custom MCP server~~ → Read tool + Python scripts via Bash

## Architecture

```
memo-agent/
├── commands/
│   └── memo.md                 # Single command: /memo
├── skills/
│   └── investment-memo/
│       └── SKILL.md            # The workflow
├── scripts/
│   ├── extract_pdf.py          # pdfplumber wrapper (20 lines)
│   └── generate_docx.py        # python-docx wrapper (50 lines)
├── templates/                  # Example memos for style reference
├── CLAUDE.md
└── README.md
```

**That's it.** No MCP servers. No agents directory. No state machine.

## How It Works

### Step 1: User Syncs Documents

```bash
# User runs this before starting (or we provide a helper)
rclone sync dropbox:Datarooms/AcmeCorp ./dataroom/
```

Why: Dropbox MCP adds OAuth complexity. rclone is battle-tested and already installed on most dev machines.

### Step 2: User Starts Memo

```
/memo ./dataroom/
```

### Step 3: Claude Reads Documents

Claude uses the Read tool for text files and shells out to `extract_pdf.py` for PDFs:

```bash
python scripts/extract_pdf.py ./dataroom/pitch-deck.pdf
```

### Step 4: Claude Proposes Materials

```markdown
## Documents Found

I found 12 documents in ./dataroom/:

**Recommended for memo:**
- pitch-deck.pdf - Company overview, financials, team
- financial-model.xlsx - Projections and scenarios
- term-sheet.pdf - Deal terms

**Skipping:**
- meeting-notes-v1.docx - Superseded by v2
- logo.png - Not relevant

Should I proceed with these? You can say "include [file]" or "exclude [file]".
```

User responds naturally: "looks good" or "also include the market-report.pdf"

### Step 5: Claude Asks About Sections

```markdown
## Memo Sections

Based on the documents and standard memo structure, I'll draft:

1. Deal Summary
2. Investment Strengths
3. Risk Factors
4. Company Analysis
5. Market Analysis
6. Financial Analysis
7. Management Overview

Want me to start with Deal Summary?
```

### Step 6: Claude Drafts Each Section

For each section:

1. Claude reads relevant source documents
2. Drafts the section with citations
3. Shows it to the user
4. User approves, edits, or asks for regeneration

```markdown
## Deal Summary (Draft)

Acme Corp is raising a $50M Series B at a $200M post-money valuation...
[Source: term-sheet.pdf, page 1]

The company has achieved $14.4M ARR with 150% YoY growth...
[Source: financial-model.xlsx, Revenue tab]

---
**Word count:** 423 | **Target:** 400-500

Approve this section? Or give me feedback to revise.
```

### Step 7: Export to Word

Once all sections are approved:

```bash
python scripts/generate_docx.py ./workspace/memo.md ./output/AcmeCorp-Memo.docx
```

## The Scripts

### extract_pdf.py (~20 lines)

```python
#!/usr/bin/env python3
"""Extract text from PDF using pdfplumber."""
import sys
import pdfplumber

def extract(path: str, max_pages: int = 50) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            text_parts.append(f"--- Page {i+1} ---")
            text_parts.append(page.extract_text() or "[No text found]")

            # Extract tables
            for table in page.extract_tables():
                text_parts.append("\n[Table]\n")
                for row in table:
                    text_parts.append(" | ".join(str(cell or "") for cell in row))

    if len(pdf.pages) > max_pages:
        text_parts.append(f"\n[Truncated: showing {max_pages} of {len(pdf.pages)} pages]")

    return "\n".join(text_parts)

if __name__ == "__main__":
    print(extract(sys.argv[1]))
```

### generate_docx.py (~50 lines)

```python
#!/usr/bin/env python3
"""Generate Word document from markdown."""
import sys
import re
from docx import Document
from docx.shared import Pt

def markdown_to_docx(md_path: str, output_path: str, template_path: str = None):
    doc = Document(template_path) if template_path else Document()

    with open(md_path) as f:
        content = f.read()

    # Split by ## headers
    sections = re.split(r'^## ', content, flags=re.MULTILINE)

    for section in sections[1:]:  # Skip content before first header
        lines = section.strip().split('\n')
        title = lines[0]
        body = '\n'.join(lines[1:]).strip()

        doc.add_heading(title, level=1)

        for para in body.split('\n\n'):
            if para.startswith('- '):
                # Bullet list
                for item in para.split('\n'):
                    doc.add_paragraph(item.lstrip('- '), style='List Bullet')
            else:
                doc.add_paragraph(para)

    doc.save(output_path)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    markdown_to_docx(sys.argv[1], sys.argv[2])
```

## The Skill

### skills/investment-memo/SKILL.md

```markdown
---
name: investment-memo
description: Draft investment memos from dataroom documents
---

# Investment Memo Skill

## Your Role

You help investment analysts draft professional investment memos. You read
source documents, draft sections one at a time, and get human approval before
proceeding.

## Workflow

1. **Read documents** - Use Read tool for .txt/.md, shell out to extract_pdf.py for PDFs
2. **Propose materials** - Show what you found, ask for approval
3. **Draft sections** - One at a time, with citations, get approval before next
4. **Export** - Generate Word doc using generate_docx.py

## Style Guide

When drafting sections:
- Professional, measured tone
- Third person ("The Company")
- Evidence-based claims with citations: [Source: filename, page X]
- Numbers: $X.XM for millions, X.X% for percentages
- Avoid superlatives without support

## Section Guidelines

### Deal Summary (400-500 words)
- Lead with transaction terms
- Key metrics upfront
- Company positioning

### Investment Strengths (600-800 words)
- 3-5 key strengths with evidence
- Competitive advantages
- Growth catalysts

### Risk Factors (500-700 words)
- Key risks with mitigations
- Use "concerns" for minor issues, "risks" for major
- Be balanced, not alarmist

### Company Analysis (500-700 words)
- Business model
- Products/services
- Brief history

### Market Analysis (500-700 words)
- TAM/SAM/SOM if available
- Competition
- Industry trends

### Financial Analysis (600-800 words)
- Historical performance
- Projections and assumptions
- Unit economics if available

### Management Overview (300-500 words)
- Key team members
- Relevant experience
- Track record

## Templates

If the user has example memos in templates/, read them first to match
their firm's style and structure.

## Workspace

Save progress to a simple workspace:

```
.memo-workspace/
├── status.txt          # Current step: "drafting:strengths"
├── materials.txt       # List of included/excluded files
├── memo.md             # The draft memo being built
└── notes.txt           # Any user decisions or context
```

If the user returns later, read status.txt to resume where they left off.
```

## The Command

### commands/memo.md

```markdown
---
name: memo
description: Create an investment memo from dataroom documents
---

# /memo Command

Start creating an investment memo.

## Usage

```
/memo [path-to-documents]
/memo ./dataroom/
/memo                    # Uses current directory
```

## What Happens

1. Reads all documents in the specified folder
2. Proposes which documents to include
3. Drafts memo sections one at a time
4. Exports to Word document

## Resuming

If a `.memo-workspace/` folder exists, asks if you want to resume or start fresh.

## Examples

```
/memo ./dataroom/acme-corp/
```

Invoke the investment-memo skill to handle the workflow.
```

## Dependencies

```
# requirements.txt
pdfplumber>=0.10.0
python-docx>=1.0.0
openpyxl>=3.1.0    # For Excel files
```

User installs once:
```bash
pip install -r requirements.txt
```

## Implementation Timeline

### Week 1: Core Flow
- [x] Plugin scaffold (commands/, skills/, scripts/)
- [x] extract_pdf.py script
- [x] generate_docx.py script
- [x] Basic skill that reads docs and drafts sections

### Week 2: Polish & Test
- [x] Workspace persistence (status.txt, memo.md) - defined in SKILL.md
- [x] Resume capability - defined in SKILL.md
- [x] Excel extraction (openpyxl)
- [ ] Test with real dataroom
- [x] README with setup instructions

**Total: 2 weeks**

## What We're NOT Building (Yet)

| Feature | Why Deferred | Add When |
|---------|--------------|----------|
| Dropbox MCP integration | OAuth complexity | Users request it |
| Custom document processor MCP | Overkill for v1 | Scale issues appear |
| State machine | Simple tracker works | Complex workflows needed |
| Style Guardian agent | Prompts are enough | Consistency issues appear |
| Learning/compounding | No user feedback yet | Users request it |
| Parallel processing | Sequential is fine | Performance issues appear |
| MNPI protocol | Local tool, user has access | Compliance requires it |
| Audit logging | Not requested | Compliance requires it |
| Multi-user sync | Single user tool | Team features needed |

## Success Criteria

MVP is successful if:
- [ ] Analyst can create a complete memo in < 1 hour (vs 4-8 hours manually)
- [ ] Output quality matches their existing memos
- [ ] Workflow feels natural, not like fighting a system
- [ ] Can resume interrupted sessions

## Comparison: Original vs MVP

| Aspect | Original Plan | MVP |
|--------|---------------|-----|
| Lines of plan | 1,600 | ~300 |
| Implementation estimate | 12 weeks | 2 weeks |
| MCP servers | 2 (custom) | 0 |
| Agents | 2 (section-writer, style-guardian) | 0 (skill only) |
| Skills | 1 (complex) | 1 (simple) |
| Commands | 1 with subcommands | 1 simple |
| State management | Pydantic + state machine | status.txt |
| Checkpoint tools | 13 MCP tools | Natural conversation |
| Security features | MNPI, audit, secure delete | None (defer) |
| Learning system | Central sync, git-based | Templates folder |
| Document processing | Custom MCP server | 20-line Python script |
| Word generation | Custom MCP server | 50-line Python script |

## Future Iterations

**v1.1** (if users request):
- Dropbox integration via rclone wrapper command
- Better Excel/PowerPoint extraction

**v1.2** (if consistency issues):
- Style checking pass (can be simple grep patterns, not an agent)

**v2.0** (if compliance requires):
- Audit logging
- Credential management via keychain

**v3.0** (if team features needed):
- Multi-user support
- Learning sync

---

## The Philosophy

> "The best code is no code. The second best is simple code that works."

This MVP embodies:
- **YAGNI**: Build only what's needed today
- **Convention over configuration**: One way to do things
- **Trust the user**: They already have access to these files
- **Ship and iterate**: Learn from real usage, not speculation

The goal is a working memo assistant in 2 weeks, not a perfect system in 12.
