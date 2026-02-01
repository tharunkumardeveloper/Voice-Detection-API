# Deployment Guide

## Prerequisites

1. Vercel account (sign up at vercel.com)
2. OpenAI API key (from platform.openai.com)
3. Vercel CLI installed: `npm i -g vercel`

## Step-by-Step Deployment

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables

In your Vercel project dashboard or via CLI:

```bash
vercel env add OPENAI_API_KEY
# Paste your OpenAI API key

vercel env add API_KEY
# Create a secure API key for authentication
```

### 4. Deploy
```bash
cd "Voice Detection API"
vercel --prod
```

### 5. Test Your Deployment

After deployment, you'll get a URL like: `https://your-project.vercel.app`

Test the health endpoint:
```bash
curl https://your-project.vercel.app/health
```

Test the detection endpoint:
```bash
curl -X POST https://your-project.vercel.app/detect \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio": "BASE64_ENCODED_AUDIO",
    "language": "english"
  }'
```

## Local Testing

Run locally before deploying:

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Then test at `http://localhost:8000`

## Troubleshooting

### Issue: Module not found
- Ensure all dependencies are in requirements.txt
- Vercel automatically installs them

### Issue: API key not working
- Check environment variables in Vercel dashboard
- Redeploy after adding env vars

### Issue: Timeout errors
- Vercel free tier has 10s timeout for serverless functions
- Consider upgrading or optimizing audio processing

## Performance Tips

1. Keep audio files under 10MB
2. Use MP3 format for smaller file sizes
3. Consider caching results for identical audio
4. Monitor OpenAI API usage and costs

## Security

- Never commit .env file
- Rotate API keys regularly
- Use strong, random API keys
- Monitor API usage for abuse
