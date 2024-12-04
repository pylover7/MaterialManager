# coding=utf-8
# @FileName  :area.py
# @Time      :2024/6/7 下午3:25
# @Author    :dayezi
from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import fields

from .base import BaseModel, TimestampMixin, UUIDModel

if TYPE_CHECKING:
    from .users import Role


class MaterialArea(BaseModel, TimestampMixin, UUIDModel):
    name = fields.CharField(max_length=50, unique=True, description="区域名称")
    code = fields.CharField(max_length=50, unique=True, description="区域编码")
    status = fields.IntField(default=0, description="状态：启用/停用")
    remark = fields.CharField(max_length=500, null=True, blank=True, description="区域描述")

    roles: fields.ManyToManyRelation["Role"]

    class Meta:
        table = "area"

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "id")
