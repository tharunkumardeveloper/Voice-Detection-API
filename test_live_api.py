import requests
import base64
import json

# Update these with your actual values
API_URL = "https://your-vercel-url.vercel.app/detect"  # Replace with your Vercel URL
API_KEY = "vda_2026_secure_key_a8f3d9c1b7e4f2a6"

def test_with_sample_audio():
    """Test the API with a sample audio file"""
    
    # You need to provide an actual MP3 file path
    audio_file_path = "sample.mp3"  # Replace with your audio file
    
    try:
        # Read and encode audio
        with open(audio_file_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Prepare request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "audio": audio_base64,
            "language": "english"
        }
        
        print("Sending request to API...")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
    except FileNotFoundError:
        print(f"Error: Audio file '{audio_file_path}' not found")
        print("Please provide a valid MP3 file path")
    except Exception as e:
        print(f"Error: {e}")

def test_health_endpoint():
    """Test the health endpoint"""
    health_url = API_URL.replace("/detect", "/health")
    
    print("Testing health endpoint...")
    response = requests.get(health_url)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=== AI Voice Detection API Test ===\n")
    
    # Test health first
    test_health_endpoint()
    
    # Test detection (uncomment when you have an audio file)
    # test_with_sample_audio()
    
    print("\nTo test detection:")
    print("1. Add an MP3 audio file to this directory")
    print("2. Update 'audio_file_path' in the script")
    print("3. Update 'API_URL' with your Vercel URL")
    print("4. Uncomment test_with_sample_audio() and run again")
