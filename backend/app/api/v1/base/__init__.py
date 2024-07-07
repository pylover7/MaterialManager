from fastapi import APIRouter

from .base import router

baseRouter = APIRouter()
baseRouter.include_router(router, tags=["基础模块"])

__all__ = ["baseRouter"]
