"""PDF text extraction module."""

from pathlib import Path
from typing import Dict
import PyPDF2


def extract_text(pdf_path: Path) -> Dict[str, any]:
    """
    Extract text from PDF and compute statistics.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dictionary with 'text', 'pages', 'words' keys
    """
    text_parts = []
    page_count = 0
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page_count = len(reader.pages)
        
        for page in reader.pages:
            page_text = page.extract_text()
            text_parts.append(page_text)
    
    full_text = '\n'.join(text_parts)
    word_count = len(full_text.split())
    
    return {
        'text': full_text,
        'pages': page_count,
        'words': word_count
    }
