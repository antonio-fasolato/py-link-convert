# URL Logger API

API REST Python per validare e loggare URL utilizzando FastAPI.

## Caratteristiche

- ✅ Validazione automatica delle URL usando Pydantic
- 📝 Logging delle URL in file e console
- 🚀 Framework FastAPI per performance elevate
- 📚 Documentazione automatica con Swagger UI
- ❤️ Health check endpoint

## Installazione

1. Clona o scarica il progetto
2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Avvio dell'API

```bash
python main.py
```

L'API sarà disponibile su: `http://localhost:8000`

## Endpoints Disponibili

### POST /log-url
Valida e logga una URL.

**Richiesta:**
```json
{
  "url": "https://example.com"
}
```

**Risposta (200):**
```json
{
  "message": "URL loggata con successo",
  "url": "https://example.com",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

**Errore (400):**
```json
{
  "detail": "URL non valida fornita"
}
```

### GET /
Endpoint di benvenuto.

### GET /health
Controllo dello stato dell'API.

## Esempi di Utilizzo

### Con curl:
```bash
# Testare l'endpoint principale
curl http://localhost:8000/

# Loggare una URL valida
curl -X POST "http://localhost:8000/log-url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'

# Health check
curl http://localhost:8000/health
```

### Con Python requests:
```python
import requests

# Loggare una URL
response = requests.post(
    "http://localhost:8000/log-url",
    json={"url": "https://www.example.com"}
)
print(response.json())
```

## Documentazione Interattiva

Una volta avviata l'API, puoi accedere alla documentazione interattiva:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Logging

Le URL vengono loggate in:
- **File**: `url_logs.log` (nella directory del progetto)
- **Console**: Output standard

Il formato del log include timestamp, livello e messaggio.

## Validazione URL

L'API accetta solo URL valide secondo gli standard HTTP/HTTPS. Esempi di URL valide:
- `https://www.example.com`
- `http://example.com/path?query=value`
- `https://subdomain.example.org:8080/path`

URL non valide risulteranno in un errore 400.

## Struttura del Progetto

```
.
├── main.py              # File principale dell'API
├── requirements.txt     # Dipendenze Python
├── README.md           # Documentazione
└── url_logs.log        # File di log (generato automaticamente)
```

## Requisiti

- Python 3.7+
- FastAPI
- Uvicorn
- Pydantic

## Sviluppo

Per avviare in modalità di sviluppo con reload automatico:

```bash
uvicorn main:app --reload