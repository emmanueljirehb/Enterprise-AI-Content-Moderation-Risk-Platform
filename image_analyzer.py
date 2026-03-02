# image_analyzer.py → Image duplicate + background analysis

from PIL import Image, ImageStat
import imagehash
import requests
from io import BytesIO
import sys
import os
import json

# Add root to find modules.bedrock_utils
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    from modules.bedrock_utils import resize_image_for_bedrock, call_bedrock_vision
except ImportError:
    # If standard import fails, try relative or direct path
    try:
        sys.path.append(root_dir)
        from modules.bedrock_utils import resize_image_for_bedrock, call_bedrock_vision
    except ImportError as e:
        print(f"CRITICAL: Failed to import bedrock_utils from {root_dir}: {e}")
        def resize_image_for_bedrock(*args, **kwargs): return None
        def call_bedrock_vision(*args, **kwargs): return "ERROR", {}

from config import VISION_MODEL_ID

# In-memory cache (replace with DB in production)
IMAGE_HASH_DB = {}

def get_image_data(image_url):
    try:
        response = requests.get(image_url, timeout=5)
        return Image.open(BytesIO(response.content))
    except:
        return None


def get_image_hash(img):
    try:
        if img:
            return str(imagehash.phash(img))
    except:
        pass
    return None


def is_image_duplicate(image_url):
    img = get_image_data(image_url)
    img_hash = get_image_hash(img)
    if not img_hash:
        return False

    if img_hash in IMAGE_HASH_DB:
        IMAGE_HASH_DB[img_hash] += 1
        return True
    else:
        IMAGE_HASH_DB[img_hash] = 1
        return False


def is_background_minimalistic(image_url):
    """
    Detects if an image has a minimalistic background (e.g. high brightness, low variance).
    Official luxury brand images often use white, clean backgrounds.
    """
    img = get_image_data(image_url)
    if not img:
        return False
        
    # Convert to grayscale to check brightness and variance
    gray_img = img.convert('L')
    stat = ImageStat.Stat(gray_img)
    
    mean_brightness = stat.mean[0]
    std_dev = stat.stddev[0]
    
    # Minimalistic background (like white) usually has high mean and low std dev
    # This is a heuristic.
    if mean_brightness > 200 and std_dev < 50:
        return True
    return False


def analyze_image_with_bedrock(image_url):
    """
    Uses Llama 3.2 Vision via Bedrock to detect counterfeit signals.
    Returns: bool (is_flagged), str (reason)
    """
    img_b64 = resize_image_for_bedrock(image_url)
    if not img_b64:
        return False, "IMAGE_PROCESS_ERROR"

    prompt = (
        "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n"
        "Task: Analyze this product image for signals of being a COUNTERFEIT, FAKE, or LOW-QUALITY REPLICA.\n"
        "Look for: blurred or misspelled logos, generic packaging for luxury brands, or poor manufacturing quality.\n"
        "Output ONLY a JSON object: {\"is_fake\": boolean, \"confidence\": float, \"reason\": \"string\"}\n"
        "<|image|>\n"
        "Analysis:<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        "{\"is_fake\":"
    )

    native_request = {
        "prompt": prompt,
        "images": [img_b64],
        "max_gen_len": 200,
        "temperature": 0.0
    }

    resp_text, usage = call_bedrock_vision(VISION_MODEL_ID, native_request)
    
    try:
        # Reconstruct JSON from pre-filled prompt
        full_text = '{"is_fake":' + resp_text.strip()
        if not full_text.endswith("}"):
            full_text += "}"
            
        data = json.loads(full_text)
        is_fake = data.get("is_fake", False)
        reason = data.get("reason", "Bedrock flagged image")
        
        # High confidence requirement for flagging
        if is_fake and data.get("confidence", 0) > 0.6:
            return True, reason
            
    except Exception as e:
        print(f"Bedrock Parse Error: {e}")

    return False, None