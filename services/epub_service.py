import xml2epub
import logging
from typing import List
import os.path
from .command_line_parser_service import args

logger = logging.getLogger(__name__)


class EpubService:
    """Service class for converting URLs to EPUB format"""
    
    def __init__(self):
        """
        Initialize the EpubService
        """
        self.output_directory = args.epub_output_path
    
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