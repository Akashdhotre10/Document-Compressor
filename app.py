from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os, shutil, zipfile

from PIL import Image
import fitz  # PyMuPDF
import gzip
import io
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
COMPRESSED_FOLDER = 'static/compressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# Compression Logic

def compress_file(filepath):
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    original_size = os.path.getsize(filepath)

    output_filename = f"{name}_compressed{ext}"
    output_path = os.path.join(COMPRESSED_FOLDER, output_filename)

    try:
        # PDF Compression
        if ext == '.pdf':
            doc = fitz.open(filepath)
            doc.save(output_path, garbage=4, deflate=True, clean=True, incremental=False)
            doc.close()

        # Image Compression
        elif ext in ['.jpg', '.jpeg', '.png']:
            image = Image.open(filepath)
            quality = 20  # More aggressive compression
            image.save(output_path, optimize=True, quality=quality)

        # Text Compression
        elif ext == '.txt':
            with open(filepath, 'rb') as f_in, gzip.open(output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # DOCX/PPTX Compression
        elif ext in ['.docx', '.pptx']:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(filepath, arcname=os.path.basename(filepath))

        # MP4 Compression using FFmpeg
        elif ext == '.mp4':
            try:
                compression_command = [
                    'ffmpeg', '-i', filepath, '-vcodec', 'libx264', '-crf', '28', output_path
                ]
                subprocess.run(compression_command, check=True)
            except Exception as e:
                print("FFmpeg compression failed:", e)
                shutil.copy(filepath, output_path)

        # Fallback for other types
        else:
            shutil.copy(filepath, output_path)

    except Exception as e:
        print("Compression failed:", e)
        shutil.copy(filepath, output_path)

    compressed_size = os.path.getsize(output_path)

    # Enforce 50% Compression
    if compressed_size > 0.5 * original_size:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(filepath, arcname=os.path.basename(filepath))
        compressed_size = os.path.getsize(output_path)

    return output_filename, original_size, compressed_size


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    compressed_filename, original_size, compressed_size = compress_file(filepath)

    reduction_percent = round((1 - (compressed_size / original_size)) * 100, 2) if original_size else 0

    return jsonify({
        'filename': compressed_filename,
        'original_size': round(original_size / (1024 * 1024), 2),
        'compressed_size': round(compressed_size / (1024 * 1024), 2),
        'reduction': reduction_percent
    })

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(COMPRESSED_FOLDER, filename, as_attachment=True)

@app.route('/developers')
def developers():
    return render_template('developers.html')

if __name__ == '__main__':
    app.run(debug=True)
