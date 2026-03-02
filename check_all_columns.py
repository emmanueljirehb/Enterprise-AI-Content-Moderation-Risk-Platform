import os
import pandas as pd
from conn import get_engine
import sys

# Add parent dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    engine = get_engine()
    
    for table in ['services', 'provider']:
        print(f"\n--- Columns in '{table}' table ---")
        inspect_query = f"DESCRIBE {table}"
        df_cols = pd.read_sql(inspect_query, engine)
        print(df_cols[['Field', 'Type']])
    
    engine.dispose()
except Exception as e:
    print(f"Error checking DB columns: {e}")
