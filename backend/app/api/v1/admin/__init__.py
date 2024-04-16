# coding=utf-8
# @FileName  :__init__.py.py
# @Time      :2024/4/16 下午9:30
# @Author    :dayezi
from fastapi import APIRouter

from .admin import router

admin_router = APIRouter()
admin_router.include_router(router, tags=["管理员模块"])

__all__ = ["admin_router"]
