FROM python:3.12-slim AS base
RUN pip install --no-cache-dir uv

RUN apt-get update && apt-get install -y wget calibre && rm -rf /var/lib/apt/lists/*

ENV CALIBRE_CONVERT_PATH=/usr/bin/ebook-convert

WORKDIR /app

COPY pyproject.toml uv.lock* ./
# Install dependencies using UV based on your lock file
RUN uv sync --locked --all-extras

# Copy the remainder of the application code
COPY . .
ENTRYPOINT ["uv", "run", "main.py"]