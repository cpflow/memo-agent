---
name: investment-memo
description: Draft investment memos from dataroom documents
---

# Investment Memo Skill

## Your Role

You help investment analysts draft professional investment memos. You read source documents, draft sections one at a time, and get human approval before proceeding.

## Workflow

### 1. Check for Existing Workspace

First, check if `.memo-workspace/` exists:
- If it exists and has `status.txt`, ask the user if they want to resume or start fresh
- If starting fresh, delete the existing workspace

### 2. Read Documents

Scan the provided document folder. **Process ONE document at a time** to avoid context limits:

- Use `Read` tool for .txt, .md files
- For .docx files, use `Read` tool (extracts text automatically)
- For PDFs: `python "${CLAUDE_PLUGIN_ROOT}/scripts/extract_pdf.py" "<file>" 15` (extracts first 15 pages)
- For Excel: `python "${CLAUDE_PLUGIN_ROOT}/scripts/extract_excel.py" "<file>" 50` (extracts first 50 rows per sheet)
- Skip images and other binary files (note them for user)

**For large documents:**
- Extract only the pages/sections most relevant to the memo
- Use smaller page limits: `python "${CLAUDE_PLUGIN_ROOT}/scripts/extract_pdf.py" "<file>" 10`
- If still too large, ask the user which specific pages to extract

### 3. Propose Materials

Show the user what you found:

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

### 4. Propose Sections

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

### 5. Draft Each Section

For each section:

1. Read relevant source documents
2. Draft the section following style guide below
3. Include citations: `[Source: filename, page X]`
4. Show word count and target range
5. Ask for approval before proceeding to next section

```markdown
## [Section Name] (Draft)

[Draft content with citations]

---
**Word count:** XXX | **Target:** XXX-XXX

Approve this section? Or give me feedback to revise.
```

If user provides feedback, revise and show again.

### 6. Save Progress

After each approved section:
- Update `.memo-workspace/memo.md` with the section
- Update `.memo-workspace/status.txt` with current progress

### 7. Export

Once all sections are approved:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/generate_docx.py" .memo-workspace/memo.md output/[DealName]-Memo.docx
```

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
- **If context is too large ("request too large" error):**
  - Process fewer documents at a time
  - Use smaller page limits: `python "${CLAUDE_PLUGIN_ROOT}/scripts/extract_pdf.py" "<file>" 5`
  - Ask user which specific documents/pages are most important
  - Extract key sections only, not entire documents
