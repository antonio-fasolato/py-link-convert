from fastapi import FastAPI, Depends
import logging
import uvicorn
import os
import argparse

from routes import health, convert, history
from security.auth import handle_api_key
from services import SqliteService

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Inizializzazione FastAPI
app = FastAPI(
    title="URL to Epub converter",
    description="REST API to convert a url to an Epub document",
    version="1.0.0"
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
args = parser.parse_args()

if __name__ == "__main__":
    if args.create_api_key:
        logger.info("Creating a new api-key")
        new_key = sqlite_service.create_new_api_key(args.create_api_key)
        logger.info(f'Created new key: {new_key}')
    else:
        # Ottenimento parametri host e port dalle variabili d'ambiente
        host = os.getenv('UVICORN_HOST', '0.0.0.0')
        port = int(os.getenv('UVICORN_PORT', '8000'))

        uvicorn.run("main:app", host=host, port=port, reload=True)