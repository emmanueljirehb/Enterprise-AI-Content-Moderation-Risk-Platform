# detection_engine.py → Orchestrates weighted scoring logic

import pandas as pd
from brand_detector import extract_brand
from price_anomaly import compute_brand_medians, is_price_anomaly
from seller_anomaly import compute_seller_stats, calculate_seller_risk_index
from scoring import contains_suspicious_text, calculate_risk, detect_brand_misuse
from image_analyzer import (
    is_image_duplicate, 
    is_background_minimalistic,
    analyze_image_with_bedrock
)
from review_analyzer import analyze_reviews
from config import WEIGHTS


def run_detection(df):
    search_cols = [col for col in ['description', 'name', 'title', 'service_name'] if col in df.columns]
    text_cols = search_cols + [c for c in ['bio', 'about'] if c in df.columns]
    
    price_col = next((c for c in ['base_price', 'discounted_price', 'price', 'amount', 'service_price'] if c in df.columns), None)
    original_price_col = next((c for c in ['mrp', 'original_price', 'was_price'] if c in df.columns), None)
    seller_col = next((c for c in ['user_id', 'seller_id'] if c in df.columns), None)
    image_col = next((c for c in ['image_url', 'profile_picture_url', 'image', 'image_path'] if c in df.columns), None)
    review_col = next((c for c in ['reviews', 'customer_reviews', 'review_text'] if c in df.columns), None)
    id_col = next((c for c in ['service_id', 'id'] if c in df.columns), None)

    df = df.copy()
    
    def safe_combine(row):
        return " ".join([str(val) for val in row if pd.notna(val) and str(val).lower() != 'nan']).strip()
    
    df["combined_text"] = df[text_cols].apply(safe_combine, axis=1)
    df["brand"] = df["combined_text"].apply(extract_brand)

    brand_medians = compute_brand_medians(df, "brand", price_col)

    seller_stats = {}
    if seller_col:
        seller_stats = compute_seller_stats(df, seller_col, "brand", price_col)

    results = []

    for _, row in df.iterrows():
        score = 0
        reasons = []

        price = row[price_col] if price_col else 0
        original_price = row[original_price_col] if original_price_col else None
        brand = row.get("brand")
        seller_id = row[seller_col] if seller_col else None
        text = row["combined_text"]
        image_url = row[image_col] if image_col else None
        reviews = row[review_col] if review_col else []

        # 1. Brand Detected
        if brand:
            score += WEIGHTS["brand_detected"]
            reasons.append("brand_detected")

        # 2. Price Anomaly (Weighted)
        if is_price_anomaly(price, brand, brand_medians, original_price):
            score += WEIGHTS["price_anomaly"]
            reasons.append("price_anomaly")

        # 3. Text Analysis (Suspicious phrases / Brand misuse)
        if contains_suspicious_text(text) or detect_brand_misuse(text, brand):
            score += WEIGHTS["suspicious_text"]
            reasons.append("suspicious_text")

        # 4. Image Analysis
        if image_url:
            if is_image_duplicate(image_url):
                score += WEIGHTS["image_duplicate"]
                reasons.append("image_duplicate")
            
            # 4.1 Bedrock Vision Analysis
            is_bedrock_fake, bedrock_reason = analyze_image_with_bedrock(image_url)
            if is_bedrock_fake:
                score += WEIGHTS.get("bedrock_vision_flag", 50)
                reasons.append(f"bedrock_vision: {bedrock_reason}")
            # Potential mitigation: If it has premium aesthetic but suspicious other signals
            # Actually premium aesthetic (minimalistic) is usually a signal of GENUINE.
            # But high similarity + low price -> counterfeit.
            # Minimalistic background check:
            # if is_background_minimalistic(image_url) and brand:
            #     # This might reduce the score if we think it's likely genuine,
            #     # but if other signals are high, we keep it.
            #     pass

        # 5. Review Analysis
        has_bad_reviews, comp_ratio = analyze_reviews(reviews if isinstance(reviews, list) else [reviews])
        if has_bad_reviews:
            score += WEIGHTS["bad_reviews"]
            reasons.append(f"bad_reviews_ratio_{comp_ratio:.2f}")

        # 6. Seller Behavior
        if seller_col:
            # Find all brands this seller has listed in this batch
            seller_brands = df[df[seller_col] == seller_id]["brand"].dropna().unique()
            seller_risk = calculate_seller_risk_index(seller_id, seller_stats, brand_medians, seller_brands)
            if seller_risk > 0:
                score += WEIGHTS["seller_risk"]
                reasons.append("seller_risk_index_high")

        risk = calculate_risk(score)

        results.append({
            "id": row[id_col] if id_col else None,
            "fake_score": score,
            "risk_level": risk,
            "reasons": reasons,
            "matched_keywords": brand,
            "entity_type": row.get("entity_type", "unknown")
        })

    return results