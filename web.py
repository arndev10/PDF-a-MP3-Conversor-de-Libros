"""Flask web interface for local testing."""

import json
import os
import tempfile
import zipfile
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from pipeline import run_pipeline, OUTPUT_DIR

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = Path('uploads')


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload."""
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
    
    for existing_pdf in app.config['UPLOAD_FOLDER'].glob('*.pdf'):
        existing_pdf.unlink()
    
    pdf_path = app.config['UPLOAD_FOLDER'] / file.filename
    file.save(pdf_path)
    
    return jsonify({
        'success': True,
        'filename': file.filename,
        'message': 'PDF uploaded successfully'
    })


@app.route('/api/convert', methods=['POST'])
def convert():
    """Run conversion pipeline."""
    upload_dir = app.config['UPLOAD_FOLDER']
    pdf_files = list(upload_dir.glob('*.pdf'))
    
    if len(pdf_files) == 0:
        return jsonify({'error': 'No PDF file found. Please upload a PDF first.'}), 400
    
    if len(pdf_files) > 1:
        return jsonify({'error': 'Multiple PDF files found'}), 400
    
    try:
        pdf_path = pdf_files[0]
        result = run_pipeline(pdf_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/files')
def list_files():
    """List generated MP3 files."""
    if not OUTPUT_DIR.exists():
        return jsonify({'files': []})
    
    audio_dir = OUTPUT_DIR / 'audio'
    if not audio_dir.exists():
        return jsonify({'files': []})
    
    mp3_files = [
        {
            'name': f.name,
            'size': f.stat().st_size
        }
        for f in audio_dir.glob('*.mp3')
    ]
    
    return jsonify({'files': mp3_files})


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download generated MP3 file."""
    audio_dir = OUTPUT_DIR / 'audio'
    return send_from_directory(str(audio_dir), filename, as_attachment=True)


@app.route('/api/clear', methods=['POST'])
def clear_audio():
    """Delete all generated MP3 files."""
    audio_dir = OUTPUT_DIR / 'audio'
    if not audio_dir.exists():
        return jsonify({'success': True, 'message': 'No hay audios para borrar', 'deleted': 0})
    deleted = 0
    for f in audio_dir.glob('*.mp3'):
        f.unlink()
        deleted += 1
    return jsonify({'success': True, 'message': f'Se borraron {deleted} archivo(s)', 'deleted': deleted})


@app.route('/api/download-zip')
def download_all_zip():
    """Download all MP3 files as a single ZIP."""
    audio_dir = OUTPUT_DIR / 'audio'
    if not audio_dir.exists():
        return jsonify({'error': 'No hay archivos de audio'}), 404
    mp3_files = list(audio_dir.glob('*.mp3'))
    if not mp3_files:
        return jsonify({'error': 'No hay archivos de audio'}), 404
    tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    try:
        with zipfile.ZipFile(tmp.name, 'w', zipfile.ZIP_DEFLATED) as zf:
            for f in mp3_files:
                zf.write(f, f.name)
        tmp.close()
        return send_file(
            tmp.name,
            mimetype='application/zip',
            as_attachment=True,
            download_name='audiolibro.zip'
        )
    finally:
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)


@app.route('/api/stats')
def get_stats():
    """Get conversion statistics."""
    stats_path = OUTPUT_DIR / 'metadata' / 'stats.json'
    if not stats_path.exists():
        return jsonify({'error': 'No stats available'}), 404
    
    stats = json.loads(stats_path.read_text(encoding='utf-8'))
    return jsonify(stats)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

