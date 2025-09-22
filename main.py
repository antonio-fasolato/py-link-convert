from fastapi import FastAPI, Depends
import logging
import uvicorn
import os
import argparse

from routes import health, convert, history
from security import handle_api_key
from services import SqliteService

# Command line parsing
parser = argparse.ArgumentParser(
    prog="py-link-sender",
    description="A script to convert links to Epub and Moby files",
    epilog='''
    The behaviour of the application can be controlled with the following environment variables:
    CALIBRE_CONVERT_PATH - The calibre bin path (on MacOS it should be something like `/Applications/calibre.app/Contents/MacOS/ebook-convert - Default is empty),
    SQLITE_PATH - The sqlite database location (important for Docker installations - Default is the current directory),
    EPUB_OUTPUT_DIRECTORY - The directory where the EPUB files will be created. (Default is the current directory),
    MOBI_OUTPUT_DIRECTORY - The directory where the MOBI files will be created. (Default is the current directory)
    '''
)
parser.add_argument(
    '-k',
    '--create-api-key',
    help='Create a new api key',
)
parser.add_argument(
    '-d',
    '--develop',
    help='Start with development configuration (verbose logging, and automatic API documentation)',
    action='store_true'
)
args = parser.parse_args()

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

        uvicorn.run("main:app", host=host, port=port, reload=True, log_level='info' if args.develop else 'error')