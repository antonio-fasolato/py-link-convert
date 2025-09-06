import xml2epub
import logging
from typing import Optional

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
    
    def url_to_epub(self, url: str, book_title: Optional[str] = None) -> str:
        """
        Convert a URL to an EPUB file
        
        Args:
            url: The URL to convert to EPUB
            book_title: Optional title for the book. If not provided, uses a default title
            
        Returns:
            str: Path to the created EPUB file
            
        Raises:
            Exception: If there's an error during the conversion process
        """
        try:
            # Use provided title or default
            title = book_title or "Web Article"
            
            # Create an empty eBook with table of contents at the beginning
            book = xml2epub.Epub(title, toc_location="beginning")
            
            # Create chapter from URL
            chapter = xml2epub.create_chapter_from_url(url)
            book.add_chapter(chapter)
            
            # Create the EPUB file
            epub_path = book.create_epub(self.output_directory)
            
            logger.info(f"Successfully created EPUB from URL: {url} -> {epub_path}")
            return epub_path
            
        except Exception as e:
            logger.error(f"Error converting URL to EPUB: {url} - {str(e)}")
            raise