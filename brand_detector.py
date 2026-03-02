# brand_detector.py → Brand extraction + misspelling detection

import re
import difflib
from config import BRAND_KEYWORDS


def extract_brand(text: str):
    text = str(text).lower()
    
    # 1. Exact match with word boundaries
    for brand in BRAND_KEYWORDS:
        if re.search(r"\b" + re.escape(brand) + r"\b", text):
            return brand
            
    # 2. Detecting misspelled brand names
    # Tokenize text to check individual words
    tokens = re.findall(r'\b\w+\b', text)
    for token in tokens:
        if len(token) < 4: continue # Skip short words to avoid false positives
        
        # Check for fuzzy match
        matches = difflib.get_close_matches(token, BRAND_KEYWORDS, n=1, cutoff=0.8)
        if matches:
            return matches[0] # Return the intended brand name
            
    return None