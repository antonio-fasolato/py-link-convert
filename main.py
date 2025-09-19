from fastapi import FastAPI, Depends
import logging
import uvicorn
import os
import argparse

from routes import health, convert, history
from security.auth import handle_api_key
from services import SqliteService

# Command line parsing
parser = argparse.ArgumentParser(
    prog="py-link-sender",
    description="A script to convert links to Epub and Moby files",
    epilog="Copyright Antonio Fasolato 2025"
)
parser.add_argument(
    '-k',
    '--create-api-key',
    help='Create a new api key',
)
parser.add_argument(
    '-d',
    '--debug',
    help='Start with development configuration',
    action='store_true'
)
args = parser.parse_args()

# Logging configuration
logging.basicConfig(
    level=logging.INFO if args.debug else logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI init
title = "URL to Epub converter"
description = "REST API to convert a url to an Epub document"
version = "1.0.0"
if args.debug:
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
        # Ottenimento parametri host e port dalle variabili d'ambiente
        host = os.getenv('UVICORN_HOST', '0.0.0.0')
        port = int(os.getenv('UVICORN_PORT', '8000'))

        uvicorn.run("main:app", host=host, port=port, reload=True, log_level='info' if args.debug else 'error')