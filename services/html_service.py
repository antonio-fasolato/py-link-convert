import logging
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class HtmlService:
    """Service class to extract data from html files"""

    def __init__(self):
        """
        Initialize the EpubService

        Args:
            output_directory: Directory where the EPUB files will be saved
        """

    def get_page_title(self, url: str) -> str:
        """
        Returns a html page title, ora a default string if not possible

        Args:
            url: The URL of the html page

        Returns:
            str: The html page title

        Raises:
            Exception: If there's an error during the extraction process
        """
        try:
            x = requests.get(url)
            text = x.text
            soup = BeautifulSoup(text, 'html.parser')
            title = soup.find('title').text
            logger.info(f'Found title for url {url}: {title}')
            return title
        except Exception as e:
            logger.error(f'Cannot get title from url {url}: {e}')
