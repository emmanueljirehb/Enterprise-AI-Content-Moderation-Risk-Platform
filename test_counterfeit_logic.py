import pandas as pd
from detection_engine import run_detection

def test_counterfeit_scenarios():
    data = [
        {
            "id": 1,
            "name": "Gucii Premium Bag", # Misspelled brand
            "description": "High quality first copy", # Suspicious text
            "price": 1000,
            "mrp": 10000, # 90% discount -> Psychological scam
            "provider_id": "seller_01",
            "reviews": ["Quality is cheap", "Fake product"], # Bad reviews
            "entity_type": "product"
        },
        {
            "id": 2,
            "name": "Rolex Submariner", # Genuine-looking name
            "description": "Premium Swiss watch",
            "price": 500, # Extremely low for Rolex (median will be computed from this batch)
            "mrp": 500,
            "provider_id": "seller_02",
            "reviews": ["Great watch"],
            "entity_type": "product"
        },
        {
            "id": 3,
            "name": "Rolex Submariner",
            "description": "Original Rolex watch",
            "price": 500000, # Normal price
            "mrp": 500000,
            "provider_id": "seller_03",
            "reviews": ["Authentic"],
            "entity_type": "product"
        }
    ]
    
    df = pd.DataFrame(data)
    results = run_detection(df)
    
    for res in results:
        print(f"\nID: {res['id']}")
        print(f"Brand: {res['matched_keywords']}")
        print(f"Score: {res['fake_score']}")
        print(f"Risk: {res['risk_level']}")
        print(f"Reasons: {res['reasons']}")

if __name__ == "__main__":
    try:
        test_counterfeit_scenarios()
    except Exception as e:
        print(f"Verification Failed: {e}")
        import traceback
        traceback.print_exc()
