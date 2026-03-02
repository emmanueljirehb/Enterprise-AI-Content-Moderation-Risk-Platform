import sys
import os
import json
import pandas as pd
from datetime import datetime, timedelta

# Add root for imports
root_dir = os.path.dirname(os.getcwd())
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Add FAKE DETECTION to path
sys.path.append(os.getcwd())

from routers.moderation import ModerationRequest, run_moderation

def test_full_pipeline():
    print("--- Starting End-to-End Moderation Pipeline Test ---")
    
    # Use a timestamp from 2 days ago to ensure we catch some records
    sync_time = (datetime.now() - timedelta(days=2)).isoformat()
    request = ModerationRequest(sync_timestamp=sync_time, send_email=True)
    
    print(f"Requesting moderation for items since: {sync_time}")
    
    try:
        response = run_moderation(request)
        print("\nPipeline Response:")
        print(json.dumps(response, indent=2))
        
        if response.get("status") in ["completed", "BLOCKED"]:
            csv_path = response.get("csv_saved_at")
            if csv_path and os.path.exists(csv_path):
                print(f"\nSUCCESS: CSV report saved at {csv_path}")
                df = pd.read_csv(csv_path)
                print(f"Items in report: {len(df)}")
                if len(df) > 0:
                    print(f"Columns in report: {list(df.columns)}")
                    # Check for Bedrock reasons
                    if 'reasons' in df.columns:
                        bedrock_hits = df[df['reasons'].str.contains('bedrock', na=False)]
                        print(f"Bedrock vision hits: {len(bedrock_hits)}")
            else:
                print(f"\nWARNING: CSV report not found at {csv_path}")
        else:
            print(f"\nPipeline status: {response.get('status')}")
            
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_full_pipeline()
