# Python url to EPUB or MOBI converter

Python REST API to validate and convert urls using FastAPI, xml2epub and calibre.

## The reason behind this project

I actually use and love both [Wallabag](https://wallabag.org/) and [Calibre web automated](https://github.com/crocodilestick/Calibre-Web-Automated) a lot, but for my workflow I was missing an important step: the ability to share a link from my phone, convert it to something my e-reader could open and send it automatically to CWA. I wrote this very simple python module to expose an API I can use from my phone to achieve exactly that.

The workflow is this (still working on it):

- have this API self-hosted on a machine in my home network (publicly exposed)
- use [HTTP Shortcuts](https://http-shortcuts.rmy.ch/) to share a link from my phone to the module
- have the module convert the url to epub or mobi in a folder shared with CWA
- leverage the auto-ingest functionality of CWA to import the generated file
- Have it available in CWA

## Thanks

This is little more than glue to use the work of other great pieces of software. In no particular order:

- [xml2epub](https://pypi.org/project/xml2epub/)
- [Calibre web automated](https://github.com/crocodilestick/Calibre-Web-Automated)
- [Calibre](https://calibre-ebook.com/)

## Prerequisites

This module uses the `ebook-convert` command from Calibre, so the application must be available and executable somewhere in the machine or container where the module is running. If the executable is not present, only EPUB convertions will be available. 

## Configuration

The module can be configured in two ways:

- Command line parameters (to decide its fundamental behaviour)

```bash
uv run main.py -h                                                                                                                                                                                                       antonio.fasolato@IT-IT00058
usage: py-link-sender [-h] [-k CREATE_API_KEY] [-d]

A script to convert links to Epub and Moby files

options:
  -h, --help            show this help message and exit
  -k CREATE_API_KEY, --create-api-key CREATE_API_KEY
                        Create a new api key
  -d, --develop         Start with development configuration (verbose logging, and automatic API documentation)

Copyright Antonio Fasolato 2025
```

- Environment variables (to change its behaviour)
  - `CALIBRE_CONVERT_PATH` - The calibre bin path (on MacOS it should be something like `/Applications/calibre.app/Contents/MacOS/ebook-convert`). Default is empty
  - `SQLITE_PATH` - The sqlite database location (important for Docker installations). Default is the current directory.
  - `EPUB_OUTPUT_DIRECTORY` - The directory where the EPUB files will be created. Default is the current directory.
  - `MOBI_OUTPUT_DIRECTORY` - The directory where the MOBI files will be created. Default is the current directory.
  - `UVICORN_HOST` - Unicorv host
  - `UVICORN_PORT` - Unicorv port

## Starting the API

### Generating an api-key

Some end points are authenticated, using an api-key. to generate a new api-key the module must be called with the `-k` parameter, passing a unique username. The api-key will be created and stored in the application database. 

```bash
uv run main.py -k user
```

### Running the application

```bash
uv run main.py
```

The API will be available at: `http://localhost:8000`

Once the API is running in **development mode**, you can access the interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Docker

The application is meant to run mainly in Docker. The Dockerfile in the repository can be used to generate an image, for example with

```bash
docker build -t py-link-convert .
```

With the image ready, the module can be launched with:

```bash
docker run -td --name py-link-convert \
    -e SQLITE_PATH="/data/py-link-convert.sqlite" \
    -e EPUB_OUTPUT_DIRECTORY="/data/output" \
    -e MOBI_OUTPUT_DIRECTORY="/data/output" \
    -v "$PWD/py-link-convert.sqlite:/data/py-link-convert.sqlite" \
    -v py-link-convert-volume:/data/output \
    -p 8000:8000 \
    py-link-convert <args>
```

`<args>` are optional and are the usual module arguments (`-d`, `-k` etc)

To generate a new api-key when the container is running, you can execute (supposing the running container is called py-link-convert)

```bash
docker exec -ti py-link-convert uv run main.py -k user
```

## URL Validation

The API only accepts valid URLs according to HTTP/HTTPS standards. Examples of valid URLs:
- `https://www.example.com`
- `http://example.com/path?query=value`
- `https://subdomain.example.org:8080/path`

Invalid URLs will result in a 400 error.
