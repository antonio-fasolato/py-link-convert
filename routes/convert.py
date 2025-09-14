from fastapi import HTTPException, APIRouter
from pydantic import ValidationError
import logging
from datetime import datetime
import os
from models import URLRequest, URLResponse
from services import EpubService, HtmlService, SqliteService, MobiService
import uuid
from pathvalidate import sanitize_filename

router = APIRouter()

logger = logging.getLogger(__name__)

# Inizializzazione del servizio EPUB
epub_output_dir = os.getenv('EPUB_OUTPUT_DIRECTORY')
if epub_output_dir:
    epub_service = EpubService(output_directory=epub_output_dir)
else:
    epub_service = EpubService()

# Html service initialization
html_service = HtmlService()

# SQLite service initialization
sqlite_service = SqliteService()

mobi_output_dir = os.getenv('MOBI_OUTPUT_DIRECTORY')
if mobi_output_dir:
    mobi_service = MobiService(output_directory=mobi_output_dir)
else:
    mobi_service = MobiService()

@router.post("/convert-url-to-file", response_model=URLResponse)
async def convert_url_to_file(request: URLRequest):
    """
    Endpoint to receive a list of valid URLs and save them to Epub format in the configured path.

    Args:
        request: Object containing the list of URLs to validate and process

    Returns:
        URLResponse: Operation confirmation with details

    Raises:
        HTTPException: If any URL is not valid or if there's an error during processing
    """
    try:
        # Le URL sono già validate da Pydantic tramite HttpUrl
        url_strings = [str(url) for url in request.urls]
        timestamp = datetime.now().isoformat()

        # Log delle URL
        logger.info(f"URLs ricevute e validate: {url_strings}")

        # Convert URLs to EPUB using the service
        title = html_service.get_page_title(url_strings[0])
        filename = f'{uuid.uuid4()}-{title}' if title else uuid.uuid4()
        filename = sanitize_filename(filename)

        # Log each URL to the database
        for url in url_strings:
            try:
                sqlite_service.log_url_conversion(filename, url, timestamp)
            except Exception as e:
                logger.warning(f"Errore durante il logging dell'URL {url}: {e}")

        epub_path = epub_service.urls_to_epub(url_strings, title, filename)
        if request.mobi:
            mobi_path = mobi_service.epub_to_moby(epub_path)

        return URLResponse(
            message=f"URLs converted to EPUB successfully ({len(url_strings)} chapters created)",
            urls=url_strings,
            timestamp=timestamp,
            filename=filename,
            chapters_count=len(url_strings)
        )

    except ValidationError as e:
        logger.error(f"URL non valide ricevute: {e}")
        raise HTTPException(
            status_code=400,
            detail="Una o più URL non sono valide",
        )
    except Exception as e:
        logger.error(f"Errore durante la conversione delle URL: {e}")
        raise HTTPException(
            status_code=500,
            detail="Errore interno del server"
        )
