#!/usr/bin/env python3
"""CLI entry point for PDF to MP3 conversion."""

import sys
from pathlib import Path


def validate_input_directory(input_dir: Path) -> Path:
    """
    Validate input directory contains exactly one PDF.
    
    Args:
        input_dir: Path to input directory
        
    Returns:
        Path to the single PDF file
        
    Raises:
        SystemExit: If validation fails
    """
    if not input_dir.exists():
        print(f"Error: Directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if len(pdf_files) == 0:
        print(f"Error: No PDF file found in '{input_dir}'.", file=sys.stderr)
        sys.exit(1)
    
    if len(pdf_files) > 1:
        print(f"Error: Multiple PDF files found in '{input_dir}':", file=sys.stderr)
        for pdf in pdf_files:
            print(f"  - {pdf.name}", file=sys.stderr)
        print("Please ensure exactly one PDF file exists.", file=sys.stderr)
        sys.exit(1)
    
    return pdf_files[0]


def main():
    """Main CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_directory>", file=sys.stderr)
        sys.exit(1)
    
    input_dir = Path(sys.argv[1]).resolve()
    pdf_path = validate_input_directory(input_dir)
    
    print(f"Found PDF: {pdf_path.name}")
    print("Starting conversion pipeline...")
    
    from pipeline import run_pipeline
    run_pipeline(pdf_path)


if __name__ == "__main__":
    main()

