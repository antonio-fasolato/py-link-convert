from fastapi import FastAPI, Depends
import logging
import uvicorn
import os

from routes import health, convert, history
from security import handle_api_key
from services import SqliteService, args

# Logging configuration
logging.basicConfig(
    level=logging.INFO if args.develop else logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI init
title = "URL to Epub/Mobi converter"
description = "REST API to convert a url to an Epub document"
version = "1.0.0"
if args.develop:
    app = FastAPI(
        title= title,
        description=description,
        version=version
    )
else:
    app = FastAPI(
        title=title,
        description=description,
        version=version,
        docs_url=None,
        redoc_url=None,
        openapi_url=None
    )
app.include_router(health.router)
app.include_router(
    convert.router,
    dependencies=[Depends(handle_api_key)]
)
app.include_router(
    history.router,
    dependencies=[Depends(handle_api_key)]
)

sqlite_service = SqliteService()

if __name__ == "__main__":
    if args.create_api_key:
        logger.info("Creating a new api-key")
        new_key = sqlite_service.create_new_api_key(args.create_api_key)
        print(f'Created new key: {new_key}')
    else:
        host = os.getenv('UVICORN_HOST', '0.0.0.0')
        port = int(os.getenv('UVICORN_PORT', '8000'))

        uvicorn.run("main:app", host=host, port=port, reload=args.develop, log_level='info' if args.develop else 'error')