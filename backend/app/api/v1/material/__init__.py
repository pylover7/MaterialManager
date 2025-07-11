from fastapi import APIRouter

from .material import router
from .borrowed import borrowedRouter
from .checked import checkedRouter

materialRouter = APIRouter()
materialRouter.include_router(router, tags=["物资管理模块"])
materialRouter.include_router(
    borrowedRouter,
    tags=["物资借用模块"],
    prefix="/borrowed")
materialRouter.include_router(
    checkedRouter,
    tags=["物资送检模块"],
    prefix="/checked")

__all__ = ["materialRouter"]
