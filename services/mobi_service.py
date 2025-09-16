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

    @staticmethod
    def epub_to_moby(input_filename: str, output_filename: str):
        """
        Convert an EPUB file to a MOBI one

        Args:
            input_filename: The EPUB file

        Returns:
            str: Path to the created MOBY file

        Raises:
            Exception: If there's an error during the conversion process
        """
        command = [os.getenv('CALIBRE_CONVERT_PATH', 'ebook-convert'), input_filename, output_filename]
        logger.info(f'Running {" ".join(command)}')
        try:
            subprocess.call(command)
        except Exception as e:
            logger.error(f"Error converting URLs to MOBI: {str(e)}")
            raise
        return output_filename