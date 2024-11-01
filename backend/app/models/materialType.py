# coding=utf-8
# @FileName  :materialType.py
# @Time      :2024/6/7 下午3:24
# @Author    :dayezi
from tortoise import fields

from .base import BaseModel, TimestampMixin, UUIDModel


class MaterialType(BaseModel, TimestampMixin, UUIDModel):
    key = fields.CharField(max_length=20, description="物资类型关键字")
    name = fields.CharField(max_length=50, description="物资类型名称")

    class Meta:
        table = "material_type"

    class PydanticMeta:
        exclude = "id"

