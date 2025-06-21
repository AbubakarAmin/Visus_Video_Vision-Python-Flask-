# Visus: Video-to-Description Web App

Visus is a modern Flask web application that allows users to upload a video, extracts key frames, and sends them to a Large Language Model (LLM) API (such as Qwen via OpenRouter) to generate a natural language description of the video content. The app features a beautiful, user-friendly interface and displays both the extracted frames and the generated description.

---

## 🚀 Features
- **Video Upload:** Upload any video file directly from your browser.
- **Frame Extraction:** Automatically extracts frames at regular intervals.
- **LLM Integration:** Sends frames to a vision-capable LLM API for video understanding.
- **Modern UI:** Clean, responsive, and visually appealing frontend.
- **Results Display:** Shows both the extracted frames (in sequence) and the generated video description.

---

## 🖼️ Demo
![Demo Screenshot](static/demo_screenshot.png)

---

## 🛠️ Requirements
- Python 3.8+
- See `requirement.txt` for all Python dependencies:
  - Flask
  - opencv-python
  - openai
  - werkzeug

---

## ⚡ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/visus-video-description.git
   cd visus-video-description
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

3. **Set up your OpenRouter API key:**
   - **IMPORTANT:** You must add your own OpenRouter API key in `video_analysis.py`.
   - Remove the provided example API key from the file for security.
   - (Recommended) Use an environment variable for your API key instead of hardcoding it.

4. **Run the app:**
   ```bash
   flask run
   ```
   The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ✨ Usage
1. Open the web app in your browser.
2. Upload a video file.
3. Wait for processing (frames will be extracted and sent to the LLM API).
4. View the extracted frames and the generated video description on the results page.

---

## 🧩 Project Structure
```
├── app.py                # Main Flask app
├── video_analysis.py     # Frame extraction & LLM API logic
├── templates/
│   └── index.html        # Main frontend template
├── static/
│   ├── style.css         # Custom styles
│   └── frames/           # Extracted frames (served as static files)
├── requirement.txt       # Python dependencies
└── README.md             # This file
```

---

## 🤖 LLM API Integration
- Uses OpenRouter's API with a vision-capable model (e.g., Qwen2.5-VL).
- Make sure your API key and model name are correct and support image input.

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
[MIT](LICENSE) 