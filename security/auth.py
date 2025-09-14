from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader

from security.Tenant import Tenant
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

        # # Check if the user is trying to access an internal route
        # for path in internal_routes:
        #     if path in req.url.path and not api_key_data.is_internal:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN,
        #             detail="You do not have permission to access this route"
        #         )
    yield Tenant(username= api_key.username)
