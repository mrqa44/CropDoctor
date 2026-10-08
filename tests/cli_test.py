import sys
import os
import io
import json
from PIL import Image
from dotenv import load_dotenv

# Add parent dir to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.gemini_client import analyze_plant_image

# Load env variables for the API key
load_dotenv()

def create_dummy_image():
    """Creates a basic solid color image (not a plant) for testing."""
    img = Image.new('RGB', (200, 200), color=(73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

if __name__ == "__main__":
    print("--- AgriLens CLI Test ---")
    
    # Check if user provided an image path, otherwise use dummy
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        print(f"Using provided image: {img_path}")
        with open(img_path, "rb") as f:
            img_bytes = f.read()
    else:
        print("No image provided. Using a dummy blue square.")
        print("(This should test our safety rule: it should detect it's NOT a plant)")
        img_bytes = create_dummy_image()
        
    print("\nSending to Gemini API... (Language: Urdu, Crop: Wheat)")
    
    # Call our service
    result = analyze_plant_image(img_bytes, crop_type="Wheat", language="Urdu")
    
    print("\n--- Result ---")
    print(json.dumps(result, indent=2, ensure_ascii=False))
