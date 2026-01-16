"""Audio encoding module for WAV to MP3 conversion."""

from pathlib import Path
from pydub import AudioSegment


def encode_mp3(wav_path: Path, mp3_path: Path) -> None:
    """
    Convert WAV file to MP3.
    
    Args:
        wav_path: Path to WAV file
        mp3_path: Path to save MP3 file
    """
    audio = AudioSegment.from_wav(str(wav_path))
    audio = audio.set_channels(1)
    
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    
    audio.export(str(mp3_path), format='mp3', bitrate='64k')
