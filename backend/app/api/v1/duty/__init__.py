# coding=utf-8
# @FileName  :__init__.py.py
# @Time      :2024/7/6 下午7:30
# @Author    :dayezi
from fastapi import APIRouter

from .duty import router
from .logs import logRouter

dutyRouter = APIRouter()
dutyRouter.include_router(router, tags=["值班模块"])
dutyRouter.include_router(logRouter, tags=["操作日志模块"], prefix="/logs")

__all__ = ["dutyRouter"]
