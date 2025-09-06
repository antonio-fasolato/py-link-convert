import xml2epub
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class EpubService:
    """Service class for converting URLs to EPUB format"""
    
    def __init__(self, output_directory: str = "/Users/antonio.fasolato/tmp"):
        """
        Initialize the EpubService
        
        Args:
            output_directory: Directory where the EPUB files will be saved
        """
        self.output_directory = output_directory
    
    def urls_to_epub(self, urls: List[str], book_title: Optional[str] = None) -> str:
        """
        Convert a list of URLs to a single EPUB file with multiple chapters
        
        Args:
            urls: List of URLs to convert to EPUB chapters
            book_title: Optional title for the book. If not provided, uses a default title
            
        Returns:
            str: Path to the created EPUB file
            
        Raises:
            Exception: If there's an error during the conversion process
        """
        try:
            # Check if the list is empty
            if not urls:
                raise ValueError("La lista di URL non può essere vuota")
            
            # Use provided title or default
            title = book_title or "Web Articles Collection"
            
            # Create an empty eBook with table of contents at the beginning
            book = xml2epub.Epub(title, toc_location="beginning")
            
            # Create a chapter for each URL
            chapters_created = 0
            for i, url in enumerate(urls, 1):
                try:
                    logger.info(f"Creating chapter {i} from URL: {url}")
                    chapter = xml2epub.create_chapter_from_url(url)
                    book.add_chapter(chapter)
                    chapters_created += 1
                except Exception as e:
                    logger.error(f"Error creating chapter from URL {url}: {str(e)}")
                    # Continue with other URLs even if one fails
                    continue
            
            # Check if at least one chapter was created
            if chapters_created == 0:
                raise ValueError("Nessun capitolo è stato creato con successo dalle URL fornite")
            
            # Create the EPUB file
            epub_path = book.create_epub(self.output_directory)
            
            logger.info(f"Successfully created EPUB from {chapters_created} URLs -> {epub_path}")
            return epub_path
            
        except Exception as e:
            logger.error(f"Error converting URLs to EPUB: {str(e)}")
            raise