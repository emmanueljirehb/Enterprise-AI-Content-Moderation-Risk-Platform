import os
import sys
import certifi

# Add root directory to sys.path to find 'utils' and 'modules'
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Fix SSL certificate verification issues
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from fastapi import FastAPI
from routers.moderation import router as moderation_router
from routers.notification import router as notification_router

app = FastAPI(
    title="Content Moderation API to detect fake products",
    version="1.0.0",
    description="it checks the database and reports if there are any fake or copyrighted products"
)

# Include moderation routes
app.include_router(moderation_router)
app.include_router(notification_router)

@app.get("/")
def root():
    return {"status": "running", "message": "Content Moderation API"}

if __name__ == "__main__":
    import uvicorn
    print("Starting Content Moderation API...")
    # Using 'app:app' because this file is named app.py
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
