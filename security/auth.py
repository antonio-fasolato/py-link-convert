from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from .tenant import Tenant
from services import SqliteService

api_key_header = APIKeyHeader(name="x-api-key")

sqlite_service = SqliteService()

def handle_api_key(req: Request, key: str = Security(api_key_header)):
    api_key = sqlite_service.find_api_key_by_key(key)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key"
        )
    yield Tenant(username= api_key.username)
