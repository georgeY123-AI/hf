from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import librosa
import numpy as np
import tempfile
import os
from typing import Dict
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Audio Transcription API",
    description="Upload audio files and get transcriptions using Wav2Vec2",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
tokenizer = None
device = None

def load_model():
    """Load the Wav2Vec2 model and tokenizer"""
    global model, tokenizer, device
    
    try:
        logger.info("Loading Wav2Vec2 model...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        model_name = "facebook/wav2vec2-base-960h"
        tokenizer = Wav2Vec2Tokenizer.from_pretrained(model_name)
        model = Wav2Vec2ForCTC.from_pretrained(model_name)
        model.to(device)
        model.eval()
        
        logger.info(f"Model loaded successfully on {device}")
        return True
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

def preprocess_audio(audio_path: str) -> np.ndarray:
    """Preprocess audio file for transcription"""
    try:
        # Load audio file
        audio, sample_rate = librosa.load(audio_path, sr=16000)
        
        # Normalize audio
        audio = audio / np.max(np.abs(audio))
        
        return audio
    except Exception as e:
        logger.error(f"Audio preprocessing failed: {e}")
        raise HTTPException(status_code=400, detail=f"Audio preprocessing failed: {str(e)}")

def transcribe_audio(audio: np.ndarray) -> str:
    """Transcribe audio using Wav2Vec2 model"""
    try:
        # Convert to tensor
        input_values = tokenizer(audio, return_tensors="pt", sampling_rate=16000).input_values
        input_values = input_values.to(device)
        
        # Get model predictions
        with torch.no_grad():
            logits = model(input_values).logits
        
        # Decode predictions
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = tokenizer.decode(predicted_ids[0])
        
        return transcription.lower().strip()
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    success = load_model()
    if not success:
        logger.error("Failed to load model on startup")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve a simple HTML interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Audio Transcription API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
            .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #45a049; }
            .result { background: white; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎙️ Audio Transcription Service</h1>
            <p>Upload an audio file to get its transcription</p>
            
            <div class="upload-area">
                <input type="file" id="audioFile" accept="audio/*" />
                <br><br>
                <button onclick="uploadFile()">Upload & Transcribe</button>
            </div>
            
            <div id="result" class="result" style="display:none;">
                <h3>Transcription Result:</h3>
                <p id="transcriptionText"></p>
            </div>
            
            <div id="loading" style="display:none;">
                <p>⏳ Processing audio... Please wait.</p>
            </div>
        </div>

        <script>
            async function uploadFile() {
                const fileInput = document.getElementById('audioFile');
                const file = fileInput.files[0];
                
                if (!file) {
                    alert('Please select an audio file');
                    return;
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').style.display = 'none';
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/transcribe', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('transcriptionText').textContent = data.transcription;
                        document.getElementById('result').style.display = 'block';
                    } else {
                        alert('Error: ' + data.detail);
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    try:
        model_status = "loaded" if model is not None else "not_loaded"
        device_info = str(device) if device is not None else "unknown"
        
        return {
            "status": "healthy",
            "model_status": model_status,
            "device": device_info,
            "torch_version": torch.__version__
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/transcribe")
async def transcribe_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """Transcribe uploaded audio file"""
    
    # Check if model is loaded
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check health endpoint.")
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Please upload an audio file")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        try:
            # Save uploaded file
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Process audio
            logger.info(f"Processing file: {file.filename}")
            audio = preprocess_audio(temp_file.name)
            
            # Transcribe
            transcription = transcribe_audio(audio)
            
            logger.info(f"Transcription completed for: {file.filename}")
            
            return {
                "filename": file.filename,
                "transcription": transcription,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file.name)
            except:
                pass

@app.get("/models/info")
async def model_info() -> Dict[str, str]:
    """Get information about loaded models"""
    return {
        "model_name": "facebook/wav2vec2-base-960h",
        "model_type": "Wav2Vec2ForCTC",
        "supported_sample_rate": "16000 Hz",
        "supported_formats": "wav, mp3, flac, m4a, ogg"
    }

if __name__ == "__main__":
    # Use port 8000 (common default for FastAPI)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )