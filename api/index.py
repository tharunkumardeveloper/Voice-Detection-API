from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from mangum import Mangum
import base64
import os
import tempfile
from openai import OpenAI
from typing import Literal
import json

app = FastAPI(title="AI Voice Detection API")

# Initialize OpenAI client lazily to avoid startup errors
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    return OpenAI(api_key=api_key)

VALID_API_KEY = os.getenv("API_KEY", "default-api-key-change-in-production")

SUPPORTED_LANGUAGES = ["tamil", "english", "hindi", "malayalam", "telugu"]

class AudioRequest(BaseModel):
    audio: str = Field(..., description="Base64-encoded MP3 audio")
    language: str = Field(..., description="Language of the audio")

class DetectionResponse(BaseModel):
    classification: Literal["AI-generated", "Human-generated"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str

def verify_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    if authorization.startswith("Bearer "):
        token = authorization[7:]
    else:
        token = authorization
    
    if token != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return token

def analyze_audio(audio_path: str, language: str) -> dict:
    """Analyze audio using Whisper and GPT for AI detection"""
    try:
        client = get_openai_client()
        
        # Transcribe audio
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language[:2] if language != "malayalam" else "ml"
            )
        
        # Analyze with GPT-4
        analysis_prompt = f"""Analyze this audio transcription to determine if it's AI-generated or human-generated voice.

Transcription: "{transcript.text}"
Language: {language}

Consider these factors:
1. Unnatural pauses or rhythm patterns
2. Overly perfect pronunciation
3. Lack of natural speech variations
4. Consistent tone without emotional fluctuations
5. Background noise characteristics

Provide your analysis in this exact JSON format:
{{
  "classification": "AI-generated" or "Human-generated",
  "confidence": 0.0-1.0,
  "explanation": "detailed explanation"
}}"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert in audio forensics and AI voice detection. Respond only with valid JSON."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/detect", response_model=DetectionResponse)
async def detect_voice(
    request: AudioRequest,
    authorization: str = Header(None)
):
    """Detect if audio is AI-generated or human-generated"""
    verify_api_key(authorization)
    
    # Validate language
    if request.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    
    # Decode base64 audio
    try:
        audio_data = base64.b64decode(request.audio)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio data")
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(audio_data)
        temp_path = temp_file.name
    
    try:
        result = analyze_audio(temp_path, request.language.lower())
        return DetectionResponse(**result)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "supported_languages": SUPPORTED_LANGUAGES}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Vercel serverless handler using Mangum
handler = Mangum(app)
