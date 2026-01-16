"""Text splitting module for time-based chunking."""

from typing import List


WORDS_PER_MINUTE = 150
TARGET_MINUTES = 40
WORDS_PER_PART = WORDS_PER_MINUTE * TARGET_MINUTES
MIN_PART_WORDS = 3000


def split_text(text: str) -> List[str]:
    """
    Split text into parts based on word count.
    
    Args:
        text: Full text to split
        
    Returns:
        List of text parts
    """
    words = text.split()
    parts = []
    current_part = []
    current_word_count = 0
    
    for word in words:
        current_part.append(word)
        current_word_count += 1
        
        if current_word_count >= WORDS_PER_PART:
            parts.append(' '.join(current_part))
            current_part = []
            current_word_count = 0
    
    if current_part:
        if len(parts) > 0 and current_word_count < MIN_PART_WORDS:
            parts[-1] += ' ' + ' '.join(current_part)
        else:
            parts.append(' '.join(current_part))
    
    return parts if parts else [text]
