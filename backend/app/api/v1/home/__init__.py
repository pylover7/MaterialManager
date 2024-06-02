# coding=utf-8
# @FileName  :__init__.py.py
# @Time      :2024/5/31 上午7:15
# @Author    :dayezi
from fastapi import APIRouter

from .home import router

home_router = APIRouter()
home_router.include_router(router, tags=["主页模块"])

__all__ = ["home_router"]