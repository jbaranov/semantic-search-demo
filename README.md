# Semantic Search Demo (based on <https://github.com/fastapi/full-stack-fastapi-template>)

## Requirements

* [Docker](https://www.docker.com/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Docker Compose

```console
docker compose up --build
```

## Demo

```console
# Upload a file
curl -X POST http://localhost:8001/api/v1/embedings/file -H "Content-Type: multipart/form-data" -F "file=@./backend/tests/data/test.pdf"

# Submit URL
curl -X POST http://localhost:8001/api/v1/embedings/url -H "Content-Type: application/json" -d '{"url": "https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf"}'
# Search
curl http://localhost:8001/api/v1/embedings/search -H "Content-Type: application/json" -d '{"query": "How to secure my documents?"}'
```

## Improvements

* Use OCR for text extraction from PDFs. Text extracted from digital documents is not always reliable. Also, there is always posibility to encounter scanned documents.
* Use reqursive sentence splitting using the same embedding model.
* Add bad text filtering (e.g. empty pages, empty lines, very short lines, etc.). Some of those could cause false positives.
* Play with different embedding models and chunking strategies to achive better results based on product requirements.
* Write unit tests 🥲

## General Workflow (for development)

[backend/README.md](./backend/README.md)
