#!/usr/bin/env python3
"""Extract data from Excel files using openpyxl."""
import sys
import os
from pathlib import Path

# Fix Windows encoding issues
os.environ["PYTHONIOENCODING"] = "utf-8"

def safe_print(text):
    """Print text safely, replacing unencodable characters."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))


def extract(path: str, max_rows: int = 50) -> str:
    """Extract data from an Excel file as markdown tables.

    Args:
        path: Path to the Excel file
        max_rows: Maximum rows per sheet to extract (default 50)

    Returns:
        Extracted content as markdown tables
    """
    from openpyxl import load_workbook

    file_path = Path(path)

    # Check if file exists
    if not file_path.exists():
        return f"[Error: File not found: {path}]"

    # Check file extension
    ext = file_path.suffix.lower()
    if ext == '.xls':
        return f"[Error: Old .xls format not supported. Please convert to .xlsx first, or use: pip install xlrd && python -c \"import xlrd; print(xlrd.open_workbook('{path}').sheet_names())\"]"

    if ext not in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
        return f"[Error: Unsupported file format: {ext}. Expected .xlsx or .xlsm]"

    try:
        wb = load_workbook(path, read_only=True, data_only=True)
    except Exception as e:
        error_msg = str(e)
        if "password" in error_msg.lower() or "encrypt" in error_msg.lower():
            return f"[Error: File appears to be password-protected: {path}]"
        elif "corrupt" in error_msg.lower() or "invalid" in error_msg.lower():
            return f"[Error: File appears to be corrupted: {path}]"
        else:
            return f"[Error opening Excel file: {error_msg}]"
    output_parts = []

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        output_parts.append(f"## Sheet: {sheet_name}\n")

        rows = []
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i >= max_rows:
                output_parts.append(f"\n[Truncated: showing {max_rows} rows]\n")
                break

            # Skip completely empty rows
            if all(cell is None for cell in row):
                continue

            # Convert cells to strings, handling None
            cells = [str(cell) if cell is not None else "" for cell in row]
            rows.append(cells)

        if rows:
            # Create markdown table
            # Use first row as header
            header = rows[0]
            output_parts.append("| " + " | ".join(header) + " |")
            output_parts.append("| " + " | ".join(["---"] * len(header)) + " |")

            for row in rows[1:]:
                # Pad row to match header length
                while len(row) < len(header):
                    row.append("")
                output_parts.append("| " + " | ".join(row[: len(header)]) + " |")

            output_parts.append("")  # Empty line between sheets

    wb.close()
    return "\n".join(output_parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        safe_print("Usage: python extract_excel.py <path-to-excel> [max-rows]")
        sys.exit(1)

    excel_path = sys.argv[1]
    max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    safe_print(extract(excel_path, max_rows))
