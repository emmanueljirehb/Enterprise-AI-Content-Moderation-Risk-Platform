# price_anomaly.py → Brand median + price anomaly logic

from config import BRAND_PRICE_THRESHOLD, SCAM_DISCOUNT_THRESHOLD


def compute_brand_medians(df, brand_col, price_col):
    brand_df = df[df[brand_col].notna()]
    if brand_df.empty:
        return {}
    return (
        brand_df.groupby(brand_col)[price_col]
        .median()
        .to_dict()
    )


def is_price_anomaly(price, brand, brand_medians, original_price=None):
    """
    Detects if a price is suspiciously low compared to the brand median
    or if it has a scam-like discount percentage.
    """
    # 1. Check for psychological scam (Huge discount % > 80%)
    if original_price and price and original_price > 0:
        discount = (original_price - price) / original_price
        if discount > SCAM_DISCOUNT_THRESHOLD:
            return True

    # 2. Check brand median anomaly
    if not brand:
        return False

    median_price = brand_medians.get(brand)
    if not median_price:
        return False

    return price < BRAND_PRICE_THRESHOLD * median_price