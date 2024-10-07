# General Workflow (for development)

## Install dependencies`

By default, the dependencies are managed with [uv](https://docs.astral.sh/uv/), go there and install it.

From `./backend/` you can install all the dependencies with:

```console
uv sync
```

Then you can activate the virtual environment with:

```console
source .venv/bin/activate
```

Make sure your editor is using the correct Python virtual environment, with the interpreter at `backend/.venv/bin/python`.

## Run Qdrant

```console
docker compose up qdrant
```

## Run backend

```console
cd backend
fastapi run --port 8001 --reload app/main.py
```

## Run worker

```console
cd backend
celery -A app.worker worker -l INFO
```
