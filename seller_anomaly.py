# seller_anomaly.py → Seller risk detection

from config import SELLER_LUXURY_MIN_COUNT, SELLER_PRICE_THRESHOLD


def compute_seller_stats(df, seller_col, brand_col, price_col):
    luxury_df = df[df[brand_col].notna()]

    if luxury_df.empty:
        return {}

    stats = (
        luxury_df.groupby(seller_col)[price_col]
        .agg(["count", "mean"])
        .rename(columns={"count": "luxury_count", "mean": "avg_price"})
    )

    return stats.to_dict("index")


def calculate_seller_risk_index(seller_id, seller_stats, brand_medians, brands_seen):
    """
    Assigns a risk score to a seller based on behavior.
    """
    if seller_id not in seller_stats:
        return 0
        
    stats = seller_stats[seller_id]
    risk_score = 0
    
    # 1. High volume of luxury items (suspicious for small sellers)
    if stats["luxury_count"] >= SELLER_LUXURY_MIN_COUNT:
        risk_score += 10
        
    # 2. Avg price is significantly lower than brand medians
    # Check against brands this seller has listed
    anomalous_brands = 0
    for brand in brands_seen:
        median = brand_medians.get(brand)
        if median and stats["avg_price"] < SELLER_PRICE_THRESHOLD * median:
            anomalous_brands += 1
            
    if anomalous_brands > 0:
        risk_score += 20
        
    return risk_score


def is_seller_suspicious(seller_id, brand, seller_stats, brand_medians):
    if seller_id not in seller_stats:
        return False

    stats = seller_stats[seller_id]
    median_price = brand_medians.get(brand)

    if not median_price:
        return False

    return (
        stats["luxury_count"] >= SELLER_LUXURY_MIN_COUNT
        and stats["avg_price"] < SELLER_PRICE_THRESHOLD * median_price
    )