from fastapi import APIRouter

from .material import router

material_router = APIRouter()
material_router.include_router(router, tags=["物资管理模块"])

__all__ = ["material_router"]