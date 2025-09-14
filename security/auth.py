from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader

from security.Tenant import Tenant

api_key = APIKeyHeader(name="x-api-key")

def handle_api_key(req: Request, key: str = Security(api_key)):
    if key != "tony":
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
    yield Tenant(username= "tony")
