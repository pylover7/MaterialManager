# coding=utf-8
# @FileName  :area.py
# @Time      :2024/6/9 上午9:52
# @Author    :dayezi
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import MaterialArea


MaterialAreaSchema = pydantic_model_creator(MaterialArea)


class MaterialAreaCreate(MaterialAreaSchema):
    ...


class MaterialAreaUpdate(MaterialAreaSchema):
    id: int
