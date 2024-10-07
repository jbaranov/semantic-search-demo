from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from qdrant_client import QdrantClient
from fastembed import TextEmbedding

from app.models import (
    DocumentRequest,
    DocumentResponse,
    DocumentProxy,
    SearchRequest,
    SearchResult,
)
from app.worker.tasks import process_document
from app.core.config import settings
from app.core.embeding_model import get_embedding_model
from app.core.vector_db import get_qdrant_client

router = APIRouter()


@router.post("/search")
def search(
    request: SearchRequest,
    model: TextEmbedding = Depends(get_embedding_model),
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
) -> List[SearchResult]:
    if not qdrant_client.collection_exists(settings.qdrant_collection_name):
        raise HTTPException(status_code=404, detail="Collection not found")

    result = qdrant_client.search(
        collection_name=settings.qdrant_collection_name,
        query_vector=list(model.embed([request.query]))[0],
        limit=settings.qdrant_result_count,
    )
    return result


@router.post("/file")
def process_document_from_file(
    file: UploadFile,
) -> DocumentResponse:
    doc = DocumentProxy.from_file(file)
    return process_document.delay(doc.name)


@router.post("/url")
def process_document_from_url(
    request: DocumentRequest,
) -> DocumentResponse:
    doc = DocumentProxy.from_url(request.url)
    return process_document.delay(doc.name)


@router.post("/clear")
def clear(
    qdrant_client: QdrantClient = Depends(get_qdrant_client),
) -> None:
    qdrant_client.delete_collection(collection_name=settings.qdrant_collection_name)
