#!/usr/bin/env python3
"""Extract text and tables from PDF using pdfplumber."""
import sys
import os
import pdfplumber

# Fix Windows encoding issues - set environment before any output
os.environ["PYTHONIOENCODING"] = "utf-8"

def safe_print(text):
    """Print text safely, replacing unencodable characters."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fallback: encode with replacement, then decode
        print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))


def extract(path: str, start_page: int = 1, num_pages: int = 10) -> str:
    """Extract text and tables from a PDF file.

    Args:
        path: Path to the PDF file
        start_page: Page to start from (1-indexed, default 1)
        num_pages: Number of pages to extract (default 10)

    Returns:
        Extracted text with page markers and tables
    """
    text_parts = []
    with pdfplumber.open(path) as pdf:
        total_pages = len(pdf.pages)
        start_idx = max(0, start_page - 1)  # Convert to 0-indexed
        end_idx = min(start_idx + num_pages, total_pages)

        text_parts.append(f"[Document has {total_pages} total pages. Showing pages {start_page}-{start_idx + (end_idx - start_idx)}]")

        for i in range(start_idx, end_idx):
            page = pdf.pages[i]
            text_parts.append(f"\n--- Page {i+1} ---")
            text_parts.append(page.extract_text() or "[No text found]")

            # Extract tables
            for table in page.extract_tables():
                text_parts.append("\n[Table]")
                for row in table:
                    text_parts.append(" | ".join(str(cell or "") for cell in row))

        if end_idx < total_pages:
            text_parts.append(
                f"\n[More pages available: {end_idx + 1}-{total_pages}]"
            )

    return "\n".join(text_parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        safe_print("Usage: python extract_pdf.py <path-to-pdf> [start-page] [num-pages]")
        safe_print("  start-page: Page to start from (1-indexed, default 1)")
        safe_print("  num-pages: Number of pages to extract (default 10)")
        sys.exit(1)

    pdf_path = sys.argv[1]
    start_page = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    num_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    safe_print(extract(pdf_path, start_page, num_pages))
