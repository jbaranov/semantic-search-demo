from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.core.config import settings


app = FastAPI(
    openapi_url=f"{settings.api_v1_str}/openapi.json",
)


app.include_router(api_router, prefix=settings.api_v1_str)
