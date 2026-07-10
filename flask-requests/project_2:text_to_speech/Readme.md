
# 🗣️ Text-to-Speech Web App (Python + Flask + pyttsx3)

This is a simple **web-based Text-to-Speech (TTS)** application built using **Python**, **Flask**, and the **pyttsx3** library.

It allows users to:
- Input any custom text
- Choose from available system voices
- Adjust speech rate and volume
- Listen to the spoken result directly in the browser

---

## 🚀 Features

- ✅ Offline TTS engine (no internet required)
- 🎙️ Supports multiple voices installed on the host system
- 🎚️ Customizable speech rate and volume
- 💡 Lightweight Flask backend + HTML/JavaScript frontend
- 🔊 Streams generated audio using the browser’s `<audio>` player

---

## 📦 Technologies Used

| Component     | Description                              |
|---------------|------------------------------------------|
| Python        | Core programming language                |
| Flask         | Web framework                            |
| pyttsx3       | Text-to-speech conversion engine         |
| HTML          | UI and client-side audio playback        |
| ffmpeg (opt.) | For extended audio format support (Linux)|

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/text-to-speech-webapp.git
cd text-to-speech-webapp
```

### 2. Set up a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, manually install:

```bash
pip install flask pyttsx3
```

### 4. (Linux only) Install `ffmpeg` and optional MBROLA voices

```bash
sudo apt update
sudo apt install ffmpeg mbrola mbrola-us1 mbrola-us2
```

---

## ▶️ Running the App

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🖥️ Usage

1. Type your text in the provided input box.
2. Select a voice from the dropdown.
3. Adjust the rate (words per minute) and volume.
4. Click **Play** to hear the spoken result.

---

## 📁 Project Structure

```
text-to-speech/
├── app.py              # Flask server
├── tts_engine.py       # TTS wrapper for pyttsx3
├── templates/
│   └── index.html      # Web interface (HTML + JS)
└── README.md           # Project documentation
```

---

## ❓ Troubleshooting

### Voice sounds robotic?

- You’re likely using the default `espeak` engine on Linux.
- Try installing MBROLA voices for improved sound quality.
- Or, run this on Windows/macOS for access to higher-quality built-in voices.

### Getting `ffmpeg: not found`?

Install it with:

```bash
sudo apt install ffmpeg
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Made with ❤️ by [Souhail Segni]

Feel free to reach out for questions or contributions!