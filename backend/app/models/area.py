# coding=utf-8
# @FileName  :area.py
# @Time      :2024/6/7 下午3:25
# @Author    :dayezi
from tortoise import fields

from .base import BaseModel, TimestampMixin, UUIDModel


class MaterialArea(BaseModel, TimestampMixin, UUIDModel):
    key = fields.CharField(max_length=20, description="物资区域关键字")
    name = fields.CharField(max_length=50, description="物资区域名称")

    class Meta:
        table = "material_area"

    class PydanticMeta:
        exclude = "id"
