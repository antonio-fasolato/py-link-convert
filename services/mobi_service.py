import logging
import subprocess
from .command_line_parser_service import args
from os import path

logger = logging.getLogger(__name__)


class MobiService:
    """Service class to convert an epub file to mobi"""

    def __init__(self):
        """
        Initialize the MobiService
        """
        self.output_directory=args.mobi_output_path

    def epub_to_moby(self, input_filename: str, output_filename: str):
        """
        Convert an EPUB file to a MOBI one

        Args:
            input_filename: The EPUB file
            output_filename: The mobi file name to create

        Returns:
            str: Path to the created MOBY file

        Raises:
            Exception: If there's an error during the conversion process
        """
        if not args.calibre_path:
            raise Exception("Calibre converter path not set (use --calibre-path)")
        command = [args.calibre_path, input_filename, path.join(self.output_directory, output_filename)]
        logger.info(f'Running {" ".join(command)}')
        try:
            subprocess.call(command)
        except Exception as e:
            logger.error(f"Error converting URLs to MOBI: {str(e)}")
            raise
        return output_filename