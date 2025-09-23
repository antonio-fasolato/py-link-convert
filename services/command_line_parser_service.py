import argparse

# def read_args():
parser = argparse.ArgumentParser(
    prog="py-link-sender",
    description="A script to convert links to Epub and Moby files",
    epilog='''
    The behaviour of the application can be controlled with the following environment variables:
    CALIBRE_CONVERT_PATH - The calibre bin path (on MacOS it should be something like `/Applications/calibre.app/Contents/MacOS/ebook-convert - Default is empty),
    SQLITE_PATH - The sqlite database location (important for Docker installations - Default is the current directory),
    EPUB_OUTPUT_DIRECTORY - The directory where the EPUB files will be created. (Default is the current directory),
    MOBI_OUTPUT_DIRECTORY - The directory where the MOBI files will be created. (Default is the current directory)
    '''
)

#Behaviour
parser.add_argument(
    '-k',
    '--create-api-key',
    help='Create a new api key',
)
parser.add_argument(
    '-d',
    '--develop',
    help='Start with development configuration (verbose logging, and automatic API documentation)',
    action='store_true'
)

# Configuration
parser.add_argument(
    "-c",
    "--calibre-path",
    help='The calibre bin path (on MacOS it should be something like `/Applications/calibre.app/Contents/MacOS/ebook-convert`). Default is empty'
)
parser.add_argument(
    "-s",
    "--sqlite-path",
    help='The application database path. Default is the current directory.',
    default="."
)
parser.add_argument(
    "-e",
    "--epub-output-path",
    help='The folder path where to generate EPUB files. Default is the current directory.',
    default="."
)
parser.add_argument(
    "-m",
    "--mobi-output-path",
    help='The folder path where to generate MOBI files. Default is the current directory.',
    default="."
)

args = parser.parse_args()
# global args
