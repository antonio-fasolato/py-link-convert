import xml2epub
import logging
from typing import Optional, List
import os.path

logger = logging.getLogger(__name__)


class EpubService:
    """Service class for converting URLs to EPUB format"""
    
    def __init__(self, output_directory: str = "."):
        """
        Initialize the EpubService
        
        Args:
            output_directory: Directory where the EPUB files will be saved
        """
        self.output_directory = output_directory
    
    def urls_to_epub(self, urls: List[str], title: str, filename: str) -> str:
        """
        Convert a list of URLs to a single EPUB file with multiple chapters
        
        Args:
            urls: List of URLs to convert to EPUB chapters
            title: Optional title for the book. If not provided, uses a default title
            filename: the epub file name
            
        Returns:
            str: Path to the created EPUB file
            
        Raises:
            Exception: If there's an error during the conversion process
        """
        try:
            # Check if the list is empty
            if not urls:
                raise ValueError("URL list cannot be empty")
            
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
                raise ValueError("No chapter successfully created from given URLs")
            
            # Create the EPUB file
            epub_path = book.create_epub(self.output_directory, absolute_location=os.path.join(self.output_directory, filename))
            
            logger.info(f"Successfully created EPUB from {chapters_created} URLs -> {epub_path}")
            return epub_path
            
        except Exception as e:
            logger.error(f"Error converting URLs to EPUB: {str(e)}")
            raise