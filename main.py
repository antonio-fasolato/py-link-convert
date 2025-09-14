from fastapi import FastAPI, Depends
import logging
import uvicorn
import os

from routes import health, convert
from auth import handle_api_key

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

if __name__ == "__main__":
    # Ottenimento parametri host e port dalle variabili d'ambiente
    host = os.getenv('UVICORN_HOST', '0.0.0.0')
    port = int(os.getenv('UVICORN_PORT', '8000'))
    
    uvicorn.run("main:app", host=host, port=port, reload=True)