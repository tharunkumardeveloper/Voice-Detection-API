import base64
import sys

def convert_audio_to_base64(audio_file_path):
    """Convert audio file to base64 string"""
    try:
        with open(audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()
            base64_string = base64.b64encode(audio_data).decode("utf-8")
            
        print(f"✅ Successfully converted: {audio_file_path}")
        print(f"File size: {len(audio_data)} bytes")
        print(f"Base64 length: {len(base64_string)} characters")
        print("\n" + "="*60)
        print("BASE64 OUTPUT (copy this):")
        print("="*60)
        print(base64_string)
        print("="*60)
        
        # Save to file
        output_file = audio_file_path + ".base64.txt"
        with open(output_file, "w") as f:
            f.write(base64_string)
        print(f"\n✅ Also saved to: {output_file}")
        
        return base64_string
        
    except FileNotFoundError:
        print(f"❌ Error: File '{audio_file_path}' not found")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = input("Enter audio file path (MP3): ")
    
    convert_audio_to_base64(audio_file)
