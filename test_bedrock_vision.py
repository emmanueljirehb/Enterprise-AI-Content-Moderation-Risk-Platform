import sys
import os
import requests

# Add parent directory to sys.path
root_dir = os.path.dirname(os.getcwd())
if root_dir not in sys.path:
    sys.path.append(root_dir)

from image_analyzer import analyze_image_with_bedrock, resize_image_for_bedrock

def test_bedrock_vision():
    # Real product image URL from CSV (Top quality nike shoes)
    test_url = "https://cdn.sithaapp.com/optimized/uploads/24-02-2026/da70744c-61d9-4b70-9a28-c27e0c485811.png"
    
    print(f"--- Testing with Real Product Image ---")
    print(f"URL: {test_url}")
    
    print(f"\n1. Testing resize_image_for_bedrock")
    img_b64 = resize_image_for_bedrock(test_url)
    if img_b64:
        print(f"SUCCESS: Image resized. Length: {len(img_b64)}")
        
        print("\n2. Testing full analyze_image_with_bedrock")
        is_fake, reason = analyze_image_with_bedrock(test_url)
        
        print("-" * 30)
        print(f"IS FLAGGED: {is_fake}")
        print(f"REASON: {reason}")
        print("-" * 30)
    else:
        print("FAILED: resize_image_for_bedrock returned None")
        # Check if it was a 404/403
        try:
            resp = requests.get(test_url, timeout=10)
            print(f"HTTP Status: {resp.status_code}")
        except Exception as e:
            print(f"Download Error: {e}")

if __name__ == "__main__":
    test_bedrock_vision()
