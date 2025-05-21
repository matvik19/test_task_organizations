from fastapi import Header, HTTPException
from src.common.config import API_KEY


def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
