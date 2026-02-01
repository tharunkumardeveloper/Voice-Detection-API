import requests
import base64
import json

# Configuration matching the submission tester format
API_URL = "https://your-vercel-url.vercel.app/detect"  # Replace with your Vercel URL
API_KEY = "vda_2026_secure_key_a8f3d9c1b7e4f2a6"

def test_submission_format(audio_file_path: str, language: str = "english"):
    """
    Test API using the exact format expected by the submission tester
    
    Headers: x-api-key
    Request Body: { "audio": "base64", "language": "language" }
    """
    
    try:
        # Read and encode audio file
        with open(audio_file_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")
        
        # Headers matching submission format
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        # Request body matching submission format
        payload = {
            "audio": audio_base64,
            "language": language
        }
        
        print(f"Testing API with submission format...")
        print(f"URL: {API_URL}")
        print(f"Language: {language}")
        print(f"Audio file: {audio_file_path}")
        print(f"Audio size: {len(audio_base64)} characters (base64)")
        print("\nSending request...\n")
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS! Response:")
            print(json.dumps(result, indent=2))
            
            # Validate response format
            print("\n=== Response Validation ===")
            assert "classification" in result, "Missing 'classification' field"
            assert result["classification"] in ["AI-generated", "Human-generated"], "Invalid classification value"
            assert "confidence" in result, "Missing 'confidence' field"
            assert 0.0 <= result["confidence"] <= 1.0, "Confidence must be between 0.0 and 1.0"
            assert "explanation" in result, "Missing 'explanation' field"
            print("✅ All validations passed!")
            
        else:
            print(f"\n❌ ERROR Response:")
            print(json.dumps(response.json(), indent=2))
            
    except FileNotFoundError:
        print(f"❌ Error: Audio file '{audio_file_path}' not found")
        print("Please provide a valid MP3 file path")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_all_languages(audio_file_path: str):
    """Test with all supported languages"""
    languages = ["tamil", "english", "hindi", "malayalam", "telugu"]
    
    print("=== Testing All Languages ===\n")
    for lang in languages:
        print(f"\n--- Testing {lang.upper()} ---")
        test_submission_format(audio_file_path, lang)
        print("-" * 50)

if __name__ == "__main__":
    print("=== AI Voice Detection API - Submission Format Test ===\n")
    
    # Example usage
    audio_file = "sample.mp3"  # Replace with your audio file
    
    print("INSTRUCTIONS:")
    print("1. Update API_URL with your Vercel deployment URL")
    print("2. Place an MP3 audio file in this directory")
    print("3. Update 'audio_file' variable with your file name")
    print("4. Run this script\n")
    print("=" * 60)
    
    # Uncomment to test
    # test_submission_format(audio_file, "english")
    
    # Or test all languages
    # test_all_languages(audio_file)
