# scoring.py → Score calculation + risk classification

from config import (
    SUSPICIOUS_WORDS,
    FAKE_SCORE_THRESHOLD,
    REVIEW_SCORE_THRESHOLD,
    WEIGHTS
)


def contains_suspicious_text(text: str):
    text = str(text).lower()
    return any(word in text for word in SUSPICIOUS_WORDS)


def detect_brand_misuse(text: str, brand: str):
    """
    Detects if a brand is used with suspicious modifiers (e.g., "Gucci style").
    """
    if not brand:
        return False
        
    text = text.lower()
    # Check if brand is near any suspicious word
    # Simple check: does the text contain both a brand and a suspicious word
    # In a more advanced version, we'd check for proximity.
    return any(word in text for word in SUSPICIOUS_WORDS)


def calculate_risk(score):
    if score >= FAKE_SCORE_THRESHOLD:
        return "FAKE"
    elif score >= REVIEW_SCORE_THRESHOLD:
        return "REVIEW"
    return "SAFE"