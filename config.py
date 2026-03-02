#config.py → Thresholds + keywords

VISION_MODEL_ID = "us.meta.llama3-2-11b-instruct-v1:0"

BRAND_KEYWORDS = [
    "gucci", "rolex", "titan", "louis vuitton", "chanel", "prada",
    "hermes", "dior", "burberry", "balenciaga", "versace", "fendi",
    "armani", "michael kors", "coach", "cartier", "omega", "hublot",
    "patek philippe", "audemars piguet", "tag heuer", "tissot",
    "breitling", "ray-ban", "oakley", "nike", "adidas", "jordan", "yeezy"
]

SUSPICIOUS_WORDS = [
    "inspired", "replica", "copy", "first copy", "mirror",
    "look like", "style", "aaa", "dupe", "imported", "aaa quality",
    "high quality replica", "luxury style", "premium leather"
]

# Scoring Weights
WEIGHTS = {
    "brand_detected": 20,
    "price_anomaly": 40,
    "suspicious_text": 20,
    "image_duplicate": 30,
    "bad_reviews": 30,
    "seller_risk": 30,
    "bedrock_vision_flag": 50
}

# Thresholds
BRAND_PRICE_THRESHOLD = 0.3      # < 30% of brand median
SCAM_DISCOUNT_THRESHOLD = 0.8    # > 80% discount
SELLER_PRICE_THRESHOLD = 0.4     # 40% of brand median
SELLER_LUXURY_MIN_COUNT = 5

FAKE_SCORE_THRESHOLD = 70
REVIEW_SCORE_THRESHOLD = 40

# SMTP Configuration
import os
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_RECIPIENTS = [r.strip() for r in os.getenv("EMAIL_RECIPIENTS", "").split(",") if r.strip()]
