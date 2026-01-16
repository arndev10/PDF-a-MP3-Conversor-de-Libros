"""Text-to-speech module for offline WAV generation."""

from pathlib import Path
import pyttsx3


def generate_wav(text: str, output_path: Path) -> None:
    """
    Generate WAV file from text using offline TTS.
    
    Args:
        text: Text to convert to speech
        output_path: Path to save WAV file
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()
