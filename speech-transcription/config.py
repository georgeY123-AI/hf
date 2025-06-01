"""
Configuration settings for the Audio Transcription API
"""
import os
from pathlib import Path

# API Configuration
API_TITLE = "Audio Transcription API"
API_DESCRIPTION = "Upload audio files and get transcriptions using Wav2Vec2"
API_VERSION = "1.0.0"

# Server Configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
PORT_RANGE_START = 8000
PORT_RANGE_END = 8010

# Model Configuration
MODEL_NAME = "facebook/wav2vec2-base-960h"
TARGET_SAMPLE_RATE = 16000

# File Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_AUDIO_TYPES = [
    "audio/wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/flac",
    "audio/m4a",
    "audio/ogg",
    "audio/webm"
]

ALLOWED_EXTENSIONS = [".wav", ".mp3", ".flac", ".m4a", ".ogg", ".webm"]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Environment-specific settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
RELOAD = DEBUG  # Auto-reload in debug mode