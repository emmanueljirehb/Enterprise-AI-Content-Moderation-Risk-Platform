import requests
import json

url = "http://127.0.0.1:8000/moderation/"
data = {
    "sync_timestamp": "2026-01-28T12:14:48.137Z"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
