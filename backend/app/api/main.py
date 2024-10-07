from fastapi import APIRouter

from app.api.routes import embedings, utils

api_router = APIRouter()
api_router.include_router(embedings.router, prefix="/embedings", tags=["embedings"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
