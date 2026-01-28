---
name: memo
description: Create an investment memo from dataroom documents
---

# /memo Command

Create an investment memo by reading dataroom documents and drafting sections with your approval at each step.

## Usage

```
/memo [path-to-documents]
/memo ./dataroom/
/memo                    # Uses current directory
```

## Arguments

- `path-to-documents` (optional): Path to folder containing dataroom materials. Defaults to current directory.

## What Happens

1. **Scans documents** in the specified folder (PDFs, Word docs, Excel files)
2. **Proposes materials** - shows what it found, asks for your approval
3. **Proposes structure** - suggests memo sections based on available content
4. **Drafts sections** one at a time, with citations, getting your approval before moving to the next
5. **Exports to Word** - generates a formatted .docx file

## Resuming Work

If a `.memo-workspace/` folder exists from a previous session, you'll be asked whether to resume or start fresh.

## Examples

```bash
# Start a new memo from a dataroom folder
/memo ./dataroom/acme-corp/

# Resume an existing memo
/memo ./dataroom/acme-corp/
# → "Found existing workspace. Resume where you left off?"

# Use current directory
/memo
```

## Prerequisites

Install dependencies first:
```bash
pip install -r requirements.txt
```

## Output

The final memo is saved to:
```
output/[DealName]-Memo.docx
```

## Tips

- Put example memos in `templates/` to help match your firm's style
- Use `include [filename]` or `exclude [filename]` when reviewing materials
- Give specific feedback when a section needs revision: "Make the risks section more balanced"
- You can always say "skip this section" to move on

---

*Invoke the `investment-memo` skill to handle the workflow.*
