# AI-Generated Voice Detection API

Production-ready API for detecting AI-generated vs human-generated voice samples.

## Features

- Multi-language support: Tamil, English, Hindi, Malayalam, Telugu
- API key authentication
- Base64 audio input (MP3 format)
- OpenAI Whisper for transcription
- GPT-4 for AI detection analysis
- Deployed on Vercel as serverless function

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp .env.example .env
# Edit .env with your keys
```

3. Deploy to Vercel:
```bash
vercel --prod
```

## API Usage

### Endpoint
```
POST /detect
```

### Headers
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### Request Body
```json
{
  "audio": "base64_encoded_mp3_audio",
  "language": "english"
}
```

### Response
```json
{
  "classification": "AI-generated",
  "confidence": 0.85,
  "explanation": "The audio exhibits consistent tone and lacks natural speech variations typical of human voice."
}
```

## Supported Languages
- tamil
- english
- hindi
- malayalam
- telugu

## Error Handling

- 401: Missing Authorization header
- 403: Invalid API key
- 400: Invalid input (bad base64, unsupported language)
- 500: Internal server error

## Environment Variables

Required in Vercel:
- `OPENAI_API_KEY`: Your OpenAI API key
- `API_KEY`: Your custom API key for authentication
