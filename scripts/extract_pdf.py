#!/usr/bin/env python3
"""Extract text and tables from PDF using pdfplumber."""
import sys
import io
import pdfplumber

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def extract(path: str, max_pages: int = 5) -> str:
    """Extract text and tables from a PDF file.

    Args:
        path: Path to the PDF file
        max_pages: Maximum pages to extract (default 5)

    Returns:
        Extracted text with page markers and tables
    """
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            text_parts.append(f"--- Page {i+1} ---")
            text_parts.append(page.extract_text() or "[No text found]")

            # Extract tables
            for table in page.extract_tables():
                text_parts.append("\n[Table]")
                for row in table:
                    text_parts.append(" | ".join(str(cell or "") for cell in row))

        if len(pdf.pages) > max_pages:
            text_parts.append(
                f"\n[Truncated: showing {max_pages} of {len(pdf.pages)} pages]"
            )

    return "\n".join(text_parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <path-to-pdf> [max-pages]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print(extract(pdf_path, max_pages))
