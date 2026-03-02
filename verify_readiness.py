import sys
import os
import json
import pandas as pd
from sqlalchemy import text

# Add root for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Add current dir to path
if current_dir not in sys.path:
    sys.path.append(current_dir)

from conn import get_engine
from config import VISION_MODEL_ID
from image_analyzer import analyze_image_with_bedrock

def verify_db():
    print("--- Verifying Database Connection ---")
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful.")
            
            # Check for portal_products table
            table_check = conn.execute(text("SHOW TABLES LIKE 'portal_products'"))
            if table_check.fetchone():
                print("✅ Table 'portal_products' found.")
                
                # Check record count
                count = conn.execute(text("SELECT COUNT(*) FROM portal_products"))
                print(f"📊 Total records in portal_products: {count.fetchone()[0]}")
            else:
                print("❌ Table 'portal_products' NOT found.")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def verify_bedrock():
    print("\n--- Verifying AWS Bedrock Connectivity ---")
    # Using a small public image for testing
    test_image_url = "https://raw.githubusercontent.com/boto/boto3/develop/docs/source/_static/boto3.png"
    print(f"Testing vision analysis with model: {VISION_MODEL_ID}")
    
    try:
        is_fake, reason = analyze_image_with_bedrock(test_image_url)
        print(f"✅ Bedrock communication successful. Flagged: {is_fake}, Reason: {reason}")
        return True
    except Exception as e:
        print(f"❌ Bedrock analysis failed: {e}")
        return False

if __name__ == "__main__":
    print("==========================================")
    print("   FAKE DETECTION READINESS DIAGNOSTIC    ")
    print("==========================================\n")
    
    db_ok = verify_db()
    bedrock_ok = verify_bedrock()
    
    print("\n==========================================")
    if db_ok and bedrock_ok:
        print("🚀 ALL SYSTEMS READY TO RUN")
    else:
        print("⚠️ SOME SYSTEMS FAILED VERIFICATION")
    print("==========================================")
