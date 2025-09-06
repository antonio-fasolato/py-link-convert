from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, ValidationError
import logging
from datetime import datetime
import uvicorn

# Configurazione del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('url_logs.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Inizializzazione FastAPI
app = FastAPI(
    title="URL Logger API",
    description="API REST per validare e loggare URL",
    version="1.0.0"
)

# Modello Pydantic per validare l'input
class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    message: str
    url: str
    timestamp: str

@app.get("/")
async def root():
    """Endpoint di benvenuto"""
    return {"message": "Benvenuto nell'API URL Logger"}

@app.post("/log-url", response_model=URLResponse)
async def log_url(request: URLRequest):
    """
    Endpoint per ricevere e loggare una URL valida
    
    Args:
        request: Oggetto contenente l'URL da validare e loggare
        
    Returns:
        URLResponse: Conferma dell'operazione con dettagli
        
    Raises:
        HTTPException: Se l'URL non è valida
    """
    try:
        # L'URL è già validata da Pydantic tramite HttpUrl
        url_str = str(request.url)
        timestamp = datetime.now().isoformat()
        
        # Log dell'URL
        logger.info(f"URL ricevuta e validata: {url_str}")
        
        return URLResponse(
            message="URL loggata con successo",
            url=url_str,
            timestamp=timestamp
        )
        
    except ValidationError as e:
        logger.error(f"URL non valida ricevuta: {e}")
        raise HTTPException(
            status_code=400, 
            detail="URL non valida fornita"
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