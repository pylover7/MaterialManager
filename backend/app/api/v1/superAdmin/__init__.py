# coding=utf-8
# @FileName  :__init__.py.py
# @Time      :2024/4/23 上午2:00
# @Author    :dayezi
from fastapi import APIRouter

from .depart import router

depart_router = APIRouter()
depart_router.include_router(router, tags=["部门模块"])

__all__ = ["depart_router"]
