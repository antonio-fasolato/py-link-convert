from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint per il controllo dello stato dell'API"""
    return {"status": "OK", "timestamp": datetime.now().isoformat()}
