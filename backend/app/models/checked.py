# coding=utf-8
# @FileName  :checked.py
# @Time      :2024/6/20 下午10:14
# @Author    :dayezi
from tortoise import fields

from .base import BaseModel, TimestampMixin


class Checked(BaseModel, TimestampMixin):
    area = fields.CharField(max_length=20, description="所属区域")
    type = fields.CharField(max_length=20, description="物资类型")
    material = fields.ForeignKeyField("models.Material", related_name="checked_material")
    number = fields.IntField(description="送检数量")
    toCheckUser = fields.ForeignKeyField('models.User', related_name='checked_user')
    returnStatus = fields.BooleanField(default=False, description="归还状态")
    returnDate = fields.DatetimeField(null=True, description="归还时间")
    toReturnUser = fields.ForeignKeyField('models.User', related_name='return_user', null=True)
    note = fields.CharField(max_length=200, null=True, description="备注")

    class Meta:
        table = "checked"

    class PydanticMeta:
        exclude = ("id", "created_at", "updated_at")
