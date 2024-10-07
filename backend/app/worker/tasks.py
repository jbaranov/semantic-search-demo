import os
import uuid

from typing import List

import fitz  # PyMuPDF

from celery.utils.log import get_task_logger
from celery import Task
from qdrant_client.models import Distance, VectorParams

from app.worker.celery import celery_app
from app.core.config import settings
from app.core.vector_db import get_qdrant_client
from app.core.embeding_model import get_embedding_model

logger = get_task_logger(__name__)


class ProcessDocument(Task):
    _model = None
    _qdrant_client = None

    @property
    def qdrant_client(self):
        if self._qdrant_client is None:
            self._qdrant_client = get_qdrant_client()
        return self._qdrant_client

    @property
    def model(self):
        if self._model is None:
            self._model = get_embedding_model()
        return self._model

    def run(self, doc_path: str):
        logger.info(f"Processing document: {doc_path}")

        self._init_collection()

        doc = fitz.open(doc_path)

        for page_num in range(len(doc)):
            page = doc[page_num]
            logger.info(f"Processing page {page_num + 1}")

            blocks = page.get_text("blocks", sort=False)

            block_texts = [block[4] for block in blocks]
            block_texts = self._merge_small_blocks(block_texts)

            embeddings = self.model.embed(block_texts)

            for block, embedding in zip(block_texts, embeddings):
                self.qdrant_client.upsert(
                    collection_name=settings.qdrant_collection_name,
                    points=[
                        {
                            "id": str(uuid.uuid4()),
                            "vector": embedding,
                            "payload": {
                                "text": block,
                            },
                        }
                    ],
                )

        doc.close()
        os.remove(doc_path)

        return f"Processed document: {doc_path}"

    def _init_collection(self):
        if not self.qdrant_client.collection_exists(settings.qdrant_collection_name):
            self.qdrant_client.create_collection(
                collection_name=settings.qdrant_collection_name,
                vectors_config=VectorParams(
                    size=settings.embedding_dimensions, distance=Distance.COSINE
                ),
            )

    def _merge_small_blocks(self, blocks: List[str]) -> List[str]:
        merged_blocks = []
        current_block = blocks[0]

        for block in blocks[1:]:
            if len(current_block) < 100:
                current_block += block
            else:
                merged_blocks.append(current_block)
                current_block = block

        return merged_blocks


process_document = ProcessDocument()
celery_app.register_task(process_document)
