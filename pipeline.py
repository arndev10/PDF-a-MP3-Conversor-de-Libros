"""Main orchestration pipeline."""

import json
from pathlib import Path
from typing import Dict
from extractor import extract_text
from splitter import split_text
from tts import generate_wav
from encoder import encode_mp3


OUTPUT_DIR = Path('output')
METADATA_DIR = OUTPUT_DIR / 'metadata'
TEXT_DIR = OUTPUT_DIR / 'text'
PARTS_DIR = TEXT_DIR / 'parts'
AUDIO_DIR = OUTPUT_DIR / 'audio'


def run_pipeline(pdf_path: Path) -> Dict[str, any]:
    """
    Run complete PDF to MP3 conversion pipeline.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dictionary with conversion results
    """
    book_name = pdf_path.stem
    
    print("Extracting text from PDF...")
    extraction_result = extract_text(pdf_path)
    full_text = extraction_result['text']
    page_count = extraction_result['pages']
    word_count = extraction_result['words']
    
    print(f"Extracted {page_count} pages, {word_count} words")
    
    print("Splitting text into parts...")
    parts = split_text(full_text)
    part_count = len(parts)
    
    print(f"Split into {part_count} parts")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    METADATA_DIR.mkdir(exist_ok=True)
    TEXT_DIR.mkdir(exist_ok=True)
    PARTS_DIR.mkdir(exist_ok=True)
    AUDIO_DIR.mkdir(exist_ok=True)
    
    full_text_path = TEXT_DIR / 'full_text.txt'
    if not full_text_path.exists():
        full_text_path.write_text(full_text, encoding='utf-8')
        print(f"Saved full text to {full_text_path}")
    
    estimated_minutes = word_count / 150
    
    stats = {
        'pages': page_count,
        'words': word_count,
        'estimated_minutes': round(estimated_minutes, 2),
        'parts': part_count
    }
    
    stats_path = METADATA_DIR / 'stats.json'
    stats_path.write_text(json.dumps(stats, indent=2), encoding='utf-8')
    print(f"Saved stats to {stats_path}")
    
    for i, part_text in enumerate(parts, 1):
        part_num = f"{i:02d}"
        part_text_path = PARTS_DIR / f"part_{part_num}.txt"
        
        if not part_text_path.exists():
            part_text_path.write_text(part_text, encoding='utf-8')
        
        wav_path = AUDIO_DIR / f"temp_part_{part_num}.wav"
        mp3_path = AUDIO_DIR / f"{book_name}-Part{part_num}.mp3"
        
        if not mp3_path.exists():
            print(f"Generating audio for part {i}/{part_count}...")
            generate_wav(part_text, wav_path)
            encode_mp3(wav_path, mp3_path)
            
            if wav_path.exists():
                wav_path.unlink()
            
            print(f"Created {mp3_path.name}")
        else:
            print(f"Skipping {mp3_path.name} (already exists)")
    
    print(f"\nConversion complete! Output in: {OUTPUT_DIR}")
    
    return {
        'success': True,
        'output_dir': str(OUTPUT_DIR),
        'stats': stats,
        'parts': part_count
    }
