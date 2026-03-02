# review_analyzer.py → Scan reviews for counterfeit keywords

REVIEW_COMPLAINT_KEYWORDS = [
    "fake", "duplicate", "not original", "cheap quality", "copy product",
    "not authentic", "scam", "waste of money", "avoid"
]

def analyze_reviews(reviews_list):
    """
    Scans a list of reviews for suspicious keywords.
    Returns (has_suspicious_reviews, complaint_ratio).
    """
    if not reviews_list or len(reviews_list) == 0:
        return False, 0.0
        
    complaint_count = 0
    for review in reviews_list:
        text = str(review).lower()
        if any(keyword in text for keyword in REVIEW_COMPLAINT_KEYWORDS):
            complaint_count += 1
            
    complaint_ratio = complaint_count / len(reviews_list)
    has_suspicious = complaint_count > 0
    
    return has_suspicious, complaint_ratio
