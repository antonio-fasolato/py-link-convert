import logging
import subprocess
import os

logger = logging.getLogger(__name__)


class MobiService:
    """Service class to convert an epub file to mobi"""

    def __init__(self, output_directory: str = "."):
        """
        Initialize the MobiService

        Args:
            output_directory: Directory where the MOBI files will be saved
        """
        self.output_directory=output_directory

    def epub_to_moby(self, filename: str):
        """
        Convert an EPUB file to a MOBI one

        Args:
            filename: The EPUB file

        Returns:
            str: Path to the created MOBY file

        Raises:
            Exception: If there's an error during the conversion process
        """
        output_file = filename.replace(".epub", ".mobi")
        command = [os.getenv('CALIBRE_CONVERT_PATH', 'ebook-convert'), filename, output_file]
        logger.info(f'Running {" ".join(command)}')
        try:
            subprocess.call(command)
        except Exception as e:
            logger.error(f"Error converting URLs to MOBI: {str(e)}")
            raise
        return output_file