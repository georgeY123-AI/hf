# 🎙️ Audio Transcription API

> Transform your audio files into text with AI-powered transcription using Facebook's Wav2Vec2 model

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-00a393.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🌟 What is this?

This is a **simple and powerful audio transcription service** that converts your voice recordings into text. Just upload an audio file, and get back the written transcript!

Perfect for:
- 📝 Converting voice memos to text
- 🎤 Transcribing interviews or meetings
- 📚 Making audio content searchable
- 🔍 Creating subtitles from audio
- 💬 Converting speech to text for accessibility

## ✨ Features

- 🚀 **Fast & Accurate** - Uses Facebook's state-of-the-art Wav2Vec2 AI model
- 🌐 **Easy Web Interface** - Simple drag-and-drop file upload
- 📱 **Multiple Formats** - Supports WAV, MP3, FLAC, M4A, and OGG files
- 🔧 **Developer Friendly** - Complete REST API with interactive documentation
- 🛡️ **Reliable** - Built-in health checks and error handling
- 💻 **Cross Platform** - Works on Windows, Mac, and Linux

## 🎬 Demo

### Web Interface
```
┌─────────────────────────────────────┐
│  🎙️ Audio Transcription Service     │
│                                     │
│  Upload an audio file to get its    │
│  transcription                      │
│                                     │
│  [Choose File] [Upload & Transcribe]│
│                                     │
│  ✅ Transcription Result:           │
│  "Hello, this is a test recording   │
│   for the transcription service."   │
└─────────────────────────────────────┘
```

### API Response Example
```json
{
  "filename": "my_recording.wav",
  "transcription": "hello this is a test recording for the transcription service",
  "status": "success"
}
```

## 🚀 Quick Start (For Everyone!)

### Step 1: Download the Project
1. Click the green "Code" button above
2. Select "Download ZIP"
3. Extract the ZIP file to your desired location

### Step 2: Run the Application
1. Open your terminal/command prompt
2. Navigate to the project folder:
   ```bash
   cd audio-transcription-api
   ```
3. Run the launcher:
   ```bash
   python run_app.py
   ```

### Step 3: Follow the Setup
The launcher will:
- ✅ Check if you have all required software
- 📦 Install missing components automatically (if you agree)
- 🚀 Start the service
- 🌐 Open your web browser automatically

### Step 4: Start Transcribing!
1. Your browser will open to `http://localhost:8000`
2. Click "Choose File" and select your audio file
3. Click "Upload & Transcribe"
4. Wait a few seconds and see your transcription!

## 📋 Requirements

### What You Need:
- **Python 3.8+** (Download from [python.org](https://python.org))
- **Internet connection** (for initial setup only)
- **Audio files** in supported formats

### Supported Audio Formats:
- 🎵 **WAV** - Uncompressed audio (best quality)
- 🎶 **MP3** - Most common format
- 🎼 **FLAC** - High-quality compressed audio
- 📱 **M4A** - iPhone/iTunes format
- 🔊 **OGG** - Open-source format

## 📁 Project Structure

```
audio-transcription-api/
├── 📄 main.py              # Main application
├── 🚀 run_app.py           # Easy launcher script
├── ⚙️ config.py            # Configuration settings
├── 📋 requirements.txt     # Required packages
├── 📖 README.md           # This file
└── 📁 temp/               # Temporary files (auto-created)
```

## 🔧 Advanced Usage

### For Developers

#### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface |
| `GET` | `/health` | Service status |
| `POST` | `/transcribe` | Upload & transcribe audio |
| `GET` | `/models/info` | Model information |
| `GET` | `/docs` | Interactive API documentation |

#### Example API Usage (Python)
```python
import requests

# Upload and transcribe an audio file
with open('my_audio.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/transcribe', files=files)
    
result = response.json()
print(f"Transcription: {result['transcription']}")
```

#### Example API Usage (curl)
```bash
curl -X POST "http://localhost:8000/transcribe" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@my_audio.wav"
```

### Configuration Options

Edit `config.py` to customize:
- **Model settings** - Change AI model or sample rate
- **File limits** - Adjust maximum file size
- **Server settings** - Change ports or host settings

## 🛠️ Troubleshooting

### Common Issues

#### ❌ "Port already in use"
**Solution**: The launcher automatically finds available ports. If you see this error, close other applications using the same port or restart your computer.

#### ❌ "Model failed to load"
**Solution**: 
1. Check your internet connection
2. Restart the application
3. If the problem persists, delete the `temp` folder and restart

#### ❌ "Audio file not supported"
**Solution**: Convert your audio file to WAV, MP3, or another supported format using:
- **Online**: [CloudConvert](https://cloudconvert.com/audio-converter)
- **Software**: Audacity (free), VLC Media Player

#### ❌ "Dependencies missing"
**Solution**: Run the launcher again and choose "y" when asked to install packages.

### Performance Tips

- 🎯 **Best Quality**: Use WAV files at 16kHz sample rate
- ⚡ **Faster Processing**: Keep audio files under 5 minutes
- 🔇 **Better Accuracy**: Use clear audio with minimal background noise
- 💾 **Save Resources**: Close other applications while processing large files

## 🤝 Support & Community

### Getting Help
- 🐛 **Found a bug?** Create an issue on GitHub
- ❓ **Have a question?** Check the troubleshooting section above
- 💡 **Feature request?** We'd love to hear your ideas!

### Contributing
We welcome contributions! Whether you're:
- 🐛 Reporting bugs
- 💡 Suggesting features
- 📝 Improving documentation
- 🔧 Adding code improvements

## 📊 System Requirements

### Minimum Requirements:
- **OS**: Windows 10, macOS 10.14, or Linux
- **RAM**: 4GB (8GB recommended)
- **Storage**: 2GB free space
- **Python**: 3.8 or higher

### Recommended for Best Performance:
- **RAM**: 8GB or more
- **CPU**: Multi-core processor
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster processing)

## 🔐 Privacy & Security

- 🛡️ **Your files are safe**: Audio files are processed locally on your computer
- 🗑️ **Auto-cleanup**: Temporary files are automatically deleted after processing
- 🔒 **No data collection**: We don't store or transmit your audio files
- 🏠 **Runs offline**: After initial setup, works without internet connection

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Facebook AI Research** for the Wav2Vec2 model
- **FastAPI** for the excellent web framework
- **Hugging Face** for model hosting and transformers library

## 🔄 Version History

### v1.0.0 (Current)
- 🎉 Initial release
- ✅ Web interface for easy file upload
- 🔧 REST API with Swagger documentation
- 🛡️ Health monitoring and error handling
- 📱 Support for multiple audio formats

---

<div align="center">

### Ready to start transcribing? 🚀

**[Download Now](#quick-start-for-everyone) • [View Documentation](#for-developers) • [Report Issues](#getting-help)**

*Made with ❤️ for everyone who needs accurate audio transcription*

</div>