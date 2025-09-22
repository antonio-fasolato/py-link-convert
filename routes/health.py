from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint to check API statul"""
    return {"status": "OK", "timestamp": datetime.now().isoformat()}
