---
name: investment-memo
description: Draft investment memos from dataroom documents
---

# Investment Memo Skill

## Your Role

You help investment analysts draft professional investment memos. You read source documents, draft sections one at a time, and get human approval before proceeding.

## Workflow

### 1. Setup Workspace

First, check if `.memo-workspace/` exists:
- If it exists and has `status.txt`, ask the user if they want to resume or start fresh
- If starting fresh, delete the existing workspace

Create the workspace:
```bash
mkdir -p .memo-workspace
```

### 2. Scan and Catalog Documents

First, list the files in the folder:

```bash
ls -la "<folder_path>"
```

Create `.memo-workspace/materials.txt` listing all files found.

### 3. Process Documents Using Subagents

**Use a subagent for EACH document** to avoid context limits. The subagent reads the full document in chunks and returns extracted facts.

For each document, use the Task tool:

```
Task tool with subagent_type: "general-purpose"
prompt: |
  Extract all key facts from this document for an investment memo.

  Document: <file_path>

  INSTRUCTIONS:
  1. For PDFs, use this inline Python command (change START and COUNT as needed):
     ```
     python -c "
     import pdfplumber
     START=1; COUNT=10
     with pdfplumber.open('<file>') as pdf:
         total=len(pdf.pages); print(f'[{total} pages total]')
         for i in range(START-1, min(START-1+COUNT, total)):
             print(f'--- Page {i+1} ---')
             print(pdf.pages[i].extract_text() or '[No text]')
         if START-1+COUNT < total: print(f'[More pages: {START+COUNT}-{total}]')
     "
     ```
     - First chunk: START=1, COUNT=10 (pages 1-10)
     - Second chunk: START=11, COUNT=10 (pages 11-20)
     - Continue until all pages are read

  2. For Excel, use this inline Python command:
     ```
     python -c "
     from openpyxl import load_workbook
     wb=load_workbook('<file>', read_only=True, data_only=True)
     for s in wb.sheetnames:
         print(f'## {s}')
         for i,row in enumerate(wb[s].iter_rows(values_only=True)):
             if i>=50: print('[Truncated]'); break
             if any(row): print(' | '.join(str(c or '') for c in row))
     "
     ```

  3. For Word/text files use the Read tool
  4. Process ALL chunks before returning - don't stop early

  EXTRACT AND RETURN:
  - Company name and description
  - All financial metrics (revenue, growth, margins, valuation, etc.)
  - Key dates and milestones
  - Management team names and backgrounds
  - Market size and competitive information
  - Risks mentioned
  - Any other investment-relevant facts

  FORMAT your response as:
  ## Facts from: [filename]

  ### Company Overview
  - [facts]

  ### Financial Metrics
  - [facts with specific numbers]

  ### Key People
  - [names and roles]

  ### Market/Competition
  - [facts]

  ### Risks/Concerns
  - [facts]

  ### Other Notable Information
  - [facts]

  Include page numbers for citations: [page X]
```

After each subagent returns, append its output to `.memo-workspace/notes.txt`.

**Run subagents in parallel** when possible for faster processing (use multiple Task calls in one message).

### 4. Propose Materials

After cataloging, show the user what you found:

```markdown
## Documents Found

I found X documents in [path]:

**Recommended for memo:**
- filename.pdf - Brief description of contents
- ...

**Skipping:**
- filename.png - Image file, not extractable
- ...

Should I proceed with these? You can say "include [file]" or "exclude [file]".
```

Wait for user approval before proceeding.

### 5. Propose Sections

Based on available materials, propose memo structure:

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

### 6. Draft Each Section

For each section:

1. Read `.memo-workspace/notes.txt` for extracted facts (don't re-read original documents)
2. Draft the section following style guide below
3. Include citations: `[Source: filename, page X]`
4. Show word count and target range
5. Ask for approval before proceeding to next section
6. If you need more detail from a specific document, extract just that document again

```markdown
## [Section Name] (Draft)

[Draft content with citations]

---
**Word count:** XXX | **Target:** XXX-XXX

Approve this section? Or give me feedback to revise.
```

If user provides feedback, revise and show again.

### 7. Save Progress

After each approved section:
- Update `.memo-workspace/memo.md` with the section
- Update `.memo-workspace/status.txt` with current progress

### 8. Export

Once all sections are approved:

```python
python -c "
import re
from pathlib import Path
from docx import Document

with open('.memo-workspace/memo.md', encoding='utf-8') as f:
    content = f.read()

doc = Document()
content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
title = re.match(r'^# (.+)\n', content)
if title:
    doc.add_heading(title.group(1), level=0)
    content = content[title.end():]

for section in re.split(r'^## ', content, flags=re.MULTILINE):
    section = section.strip()
    if not section: continue
    lines = section.split('\n')
    doc.add_heading(lines[0].strip(), level=1)
    for para in '\n'.join(lines[1:]).split('\n\n'):
        para = para.strip()
        if not para: continue
        if para.startswith('- '):
            for item in para.split('\n'):
                if item.strip(): doc.add_paragraph(item.lstrip('- '), style='List Bullet')
        else:
            doc.add_paragraph(para.replace('\n', ' '))

Path('output').mkdir(exist_ok=True)
doc.save('output/[DealName]-Memo.docx')
print('Saved to output/[DealName]-Memo.docx')
"
```

Replace `[DealName]` with the actual deal name.

Show the user where the file was saved.

## Style Guide

When drafting sections:

- **Tone**: Professional, measured, objective
- **Voice**: Third person ("The Company", "Management")
- **Evidence**: Back all claims with citations
- **Numbers**: Use $X.XM for millions, X.X% for percentages
- **Language**: Avoid superlatives without supporting evidence
- **Structure**: Use clear paragraphs, bullet points for lists

### Citation Format

Always cite sources:
- `[Source: filename.pdf, page X]`
- `[Source: filename.xlsx, Sheet Name]`
- `[Source: Management Interview]`

## Section Guidelines

### Deal Summary (400-500 words)
Lead with transaction terms and key metrics:
- Transaction type (Series A/B/C, etc.)
- Amount and valuation
- Key investors
- Company positioning (one line)
- Revenue/growth highlights

### Investment Strengths (600-800 words)
3-5 key strengths with evidence:
- Market opportunity
- Competitive advantages / moat
- Team and execution capability
- Growth catalysts
- Financial momentum (if positive)

### Risk Factors (500-700 words)
Key risks with mitigations:
- Use "concerns" for minor issues
- Use "risks" for major issues
- Be balanced, not alarmist
- Include mitigation strategies where available

### Company Analysis (500-700 words)
- Business model explanation
- Products/services overview
- Company history and milestones
- Current market position

### Market Analysis (500-700 words)
- TAM/SAM/SOM if available
- Competitive landscape
- Industry trends
- Market timing

### Financial Analysis (600-800 words)
- Historical revenue and growth
- Profitability / burn rate
- Projections and assumptions
- Unit economics if available
- Path to profitability

### Management Overview (300-500 words)
- Key team members and roles
- Relevant experience
- Track record
- Board composition (if notable)

## Workspace Structure

```
.memo-workspace/
├── status.txt          # Current step, e.g., "drafting:risk-factors"
├── materials.txt       # List of included/excluded files
├── memo.md             # The draft memo being built
└── notes.txt           # User decisions and context
```

### status.txt format
```
step: drafting
current_section: investment-strengths
sections_completed: deal-summary
deal_name: AcmeCorp
```

### memo.md format
```markdown
# Investment Memo: [Deal Name]

## Deal Summary

[Approved content]

## Investment Strengths

[Approved content]

...
```

## Templates

If the user has example memos in `templates/`:
1. Read them at the start of the workflow
2. Analyze their style, structure, and tone
3. Match their formatting preferences
4. Note any firm-specific conventions

## Error Handling

- If a PDF fails to extract, note it and continue with other files
- If user provides an empty folder, ask for the correct path
- If dependencies are missing, tell user to run `pip install pdfplumber python-docx openpyxl`
- **If a subagent hits context limits:**
  - Use smaller chunks (5 pages instead of 10)
  - The subagent should still process ALL chunks, just in smaller batches
- **If subagent fails:**
  - Retry with smaller chunk size
  - Note the error and continue with other documents
