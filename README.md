# URL Logger API

Python REST API to validate and log URLs using FastAPI.

## Features

- ✅ Automatic URL validation using Pydantic
- 📝 URL logging to file and console
- 🚀 FastAPI framework for high performance
- 📚 Automatic documentation with Swagger UI
- ❤️ Health check endpoint

## Installation

1. Clone or download the project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Starting the API

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

## Available Endpoints

### POST /log-url
Validates and logs a URL.

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response (200):**
```json
{
  "message": "URL logged successfully",
  "url": "https://example.com",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

**Error (400):**
```json
{
  "detail": "Invalid URL provided"
}
```

### GET /
Welcome endpoint.

### GET /health
API health check.

## Usage Examples

### With curl:
```bash
# Test the main endpoint
curl http://localhost:8000/

# Log a valid URL
curl -X POST "http://localhost:8000/log-url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'

# Health check
curl http://localhost:8000/health
```

### With Python requests:
```python
import requests

# Log a URL
response = requests.post(
    "http://localhost:8000/log-url",
    json={"url": "https://www.example.com"}
)
print(response.json())
```

## Interactive Documentation

Once the API is running, you can access the interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Logging

URLs are logged to:
- **File**: `url_logs.log` (in the project directory)
- **Console**: Standard output

The log format includes timestamp, level, and message.

## URL Validation

The API only accepts valid URLs according to HTTP/HTTPS standards. Examples of valid URLs:
- `https://www.example.com`
- `http://example.com/path?query=value`
- `https://subdomain.example.org:8080/path`

Invalid URLs will result in a 400 error.

## Project Structure

```
.
├── main.py              # Main API file
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
└── url_logs.log        # Log file (automatically generated)
```

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Pydantic

## Development

To start in development mode with automatic reload:

```bash
uvicorn main:app --reload