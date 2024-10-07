from fastembed import TextEmbedding

from app.core.config import settings


def get_embedding_model():
    return TextEmbedding(model_name=settings.embedding_model)
