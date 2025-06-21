from flask import Flask, render_template, request, url_for, redirect, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from video_analysis import extract_frames_from_video, analyze_video_from_image_urls

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./temp"
app.config['FRAME_FOLDER'] = "./static/frames"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['FRAME_FOLDER']):
    os.makedirs(app.config['FRAME_FOLDER'])

def to_url_path(path):
    # Convert Windows backslashes to forward slashes for URLs
    return path.replace(os.sep, '/')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return render_template('index.html', error="No video part in the request.")
    file = request.files['video']
    if file.filename == '':
        return render_template('index.html', error="No selected file.")
    filename = secure_filename(file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(video_path)

    # Extract frames to static/frames/<video_name>_frames
    frame_folder = os.path.join(app.config['FRAME_FOLDER'], filename + '_frames')
    os.makedirs(frame_folder, exist_ok=True)
    frame_paths = extract_frames_from_video(video_path, frame_folder, interval_ms=1000)

    # Serve frames as static files with forward slashes
    frame_urls = []
    for path in frame_paths:
        rel_path = os.path.relpath(path, 'static')
        rel_path = to_url_path(rel_path)
        url = url_for('static', filename=rel_path)
        frame_urls.append(request.host_url.rstrip('/') + url)

    # Call LLM API with frames in sequence
    description = analyze_video_from_image_urls(frame_urls)
    return render_template('index.html', description=description, frame_urls=frame_urls)
    