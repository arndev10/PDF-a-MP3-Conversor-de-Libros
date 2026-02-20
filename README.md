# PDF to MP3 — Book Converter

Offline-first application that converts PDF books into multiple MP3 audio files (~40 minutes each). Fully local processing using system TTS — no internet, no API costs.

## Features

- PDF text extraction and intelligent splitting
- Offline audio generation using system TTS voices
- MP3 conversion optimized for speech (mono, 64kbps)
- Web interface with drag & drop upload
- CLI mode for automation
- Smart cache to skip already-processed files

## Tech Stack

**Backend:** Python 3.11+, PyPDF2, pyttsx3, pydub, Flask
**System:** ffmpeg (required for MP3 encoding)

## Setup

```bash
pip install -r requirements.txt
```

ffmpeg must be installed separately:
- Windows: `choco install ffmpeg` or [ffmpeg.org](https://ffmpeg.org/download.html)
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

## Usage

### CLI

```bash
python main.py input/
```

Place a single PDF in the `input/` directory.

### Web Interface

```bash
python web.py
```

Open `http://127.0.0.1:5000` — upload PDFs via drag & drop, track progress, download MP3s.

## Output Structure

```
output/
├── metadata/stats.json        # Pages, words, estimated duration
├── text/
│   ├── full_text.txt          # Complete extracted text
│   └── parts/                 # Split by ~6,000 words each
└── audio/
    ├── Book-Part01.mp3        # ~40 min per file
    └── Book-Part02.mp3
```

## Project Structure

```
├── main.py           # CLI entry point
├── extractor.py      # PDF text extraction
├── splitter.py       # Text splitting logic
├── tts.py            # TTS audio generation
├── encoder.py        # WAV to MP3 conversion
├── pipeline.py       # Full pipeline orchestration
├── web.py            # Flask web interface
├── templates/
│   └── index.html    # Web UI
└── requirements.txt
```

## License

Open source — available for personal and educational use.
