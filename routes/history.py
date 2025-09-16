from fastapi import HTTPException, APIRouter, Depends
import logging
from models import URLResponse
from models.history_response import HistoryResponse
from security.Tenant import Tenant
from services import SqliteService
from security.auth import handle_api_key

router = APIRouter()

logger = logging.getLogger(__name__)

# SQLite service initialization
sqlite_service = SqliteService()

@router.get("/history", response_model=HistoryResponse)
async def history(tenant: Tenant = Depends(handle_api_key)):
    try:
        logs = sqlite_service.get_history(tenant.username)
        return HistoryResponse(
            message=f'{len(logs)} rows of ??',
            history=logs
        )
    except Exception as e:
        logger.error(f"Errore durante la conversione delle URL: {e}")
        raise HTTPException(
            status_code=500,
            detail="Errore interno del server"
        )
