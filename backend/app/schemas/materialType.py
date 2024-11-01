# coding=utf-8
# @FileName  :materialType.py
# @Time      :2024/6/7 下午3:27
# @Author    :dayezi
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import MaterialType


MaterialTypeSchema = pydantic_model_creator(MaterialType)


class MaterialTypeCreate(MaterialTypeSchema):
    ...


class MaterialTypeUpdate(MaterialTypeSchema):
    id: int

