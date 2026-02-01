import requests
import base64
import json

# Configuration
API_URL = "http://localhost:8000/detect"  # Change to your Vercel URL after deployment
API_KEY = "your_api_key_here"

def test_api(audio_file_path: str, language: str):
    """Test the voice detection API"""
    
    # Read and encode audio file
    with open(audio_file_path, "rb") as f:
        audio_data = base64.b64encode(f.read()).decode("utf-8")
    
    # Prepare request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio": audio_data,
        "language": language
    }
    
    # Send request
    print(f"Testing with {audio_file_path} ({language})...")
    response = requests.post(API_URL, headers=headers, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

if __name__ == "__main__":
    # Example usage
    # test_api("sample_audio.mp3", "english")
    print("Update API_URL and API_KEY, then uncomment test_api() call")
