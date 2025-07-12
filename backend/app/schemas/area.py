# coding=utf-8
# @FileName  :area.py
# @Time      :2024/6/9 上午9:52
# @Author    :dayezi
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel


class AreaCreate(BaseModel):
    uuid: str = None
    name: str
    code: str
    status: int = 0
    remark: str = None


class AreaUpdate(BaseModel):
    id: int
    uuid: str = None
    name: str = None
    code: str = None
    status: int = None
    remark: str = None
