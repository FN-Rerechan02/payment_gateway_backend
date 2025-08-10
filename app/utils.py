from fastapi import Header, HTTPException
from app.config import settings

def require_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != settings.app_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")
