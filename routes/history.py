from fastapi import HTTPException, APIRouter, Depends
import logging
from models import HistoryResponse
from security import Tenant, handle_api_key
from services import SqliteService

router = APIRouter()

logger = logging.getLogger(__name__)

# SQLite service initialization
sqlite_service = SqliteService()

@router.get("/history", response_model=HistoryResponse)
async def history(rows_per_page: int, page: int, tenant: Tenant = Depends(handle_api_key)):
    """
        Endpoint to get the past converted urls

    Args:
        rows_per_page: pagination: rows per page returned
        page: pagination: 0-based page returned
        tenant: Authenticated user

    Returns:
        HistoryResponse: List of previous urls

    Raises:
        HTTPException: If any URL is not valid or if there's an error during processing
    """
    try:
        count = sqlite_service.count_history(tenant.username)
        logs = sqlite_service.get_history(tenant.username, rows_per_page, page)
        return HistoryResponse(
            message=f'{len(logs)} rows of {count}',
            history=logs
        )
    except Exception as e:
        logger.error(f"Errore retrieving history: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
