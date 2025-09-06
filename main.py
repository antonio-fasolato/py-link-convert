from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
import logging
from datetime import datetime
import uvicorn
from models import URLRequest, URLResponse
from services import EpubService

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('url_logs.log'),
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

# Inizializzazione del servizio EPUB
epub_service = EpubService()

@app.post("/convert-url-to-file", response_model=URLResponse)
async def convert_url_to_file(request: URLRequest):
    """
    Endpoint to receive a valid URL and save it to Epub format in the configured path.
    
    Args:
        request: Object containing the URL to validate and log
        
    Returns:
        URLResponse: Operation confirmation with details
        
    Raises:
        HTTPException: If the URL is not valid
    """
    try:
        # L'URL è già validata da Pydantic tramite HttpUrl
        url_str = str(request.url)
        timestamp = datetime.now().isoformat()
        
        # Log dell'URL
        logger.info(f"URL ricevuta e validata: {url_str}")

        # Convert URL to EPUB using the service
        filename = "Web Article"
        epub_path = epub_service.url_to_epub(url_str, filename)

        return URLResponse(
            message="URL converted to EPUB successfully",
            url=url_str,
            timestamp=timestamp,
            filename=filename
        )
        
    except ValidationError as e:
        logger.error(f"URL non valida ricevuta: {e}")
        raise HTTPException(
            status_code=400, 
            detail="URL non valida fornita",
        )
    except Exception as e:
        logger.error(f"Errore durante il logging dell'URL: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Errore interno del server"
        )

@app.get("/health")
async def health_check():
    """Endpoint per il controllo dello stato dell'API"""
    return {"status": "OK", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)