# coding=utf-8
# @FileName  :borrowed.py
# @Time      :2024/5/31 上午12:32
# @Author    :dayezi
from tortoise import fields

from .base import BaseModel, UUIDModel


class Borrowed(BaseModel, UUIDModel):
    borrowing = fields.IntField(description="借用数量")
    username = fields.CharField(max_length=20, description="借用人名称")
    uuid = fields.UUIDField(pk=False, description="借用人uuid")
    phone = fields.CharField(max_length=20, description="借用人手机号")
    userDepart = fields.CharField(max_length=20, description="借用人部门")
    borrowTime = fields.DatetimeField(auto_now=True, description="借用时间")
    borrowApproveStatus = fields.BooleanField(default=False, description="借用批准状态")
    borrowApproveTime = fields.DatetimeField(null=True, description="借用批准时间")
    returnTime = fields.DatetimeField(null=True, description="归还时间")
    returnApproveStatus = fields.BooleanField(default=False, description="归还批准状态")
    returnApproveTime = fields.DatetimeField(null=True, description="归还批准时间")

    material = fields.ManyToManyField('models.Material', related_name='borrowed_material')
    borrowApproveUser = fields.ManyToManyField('models.User', related_name='borrowed_approve_user')
    returnApproveUser = fields.ManyToManyField('models.User', related_name='return_approve_user')

    class Meta:
        table = "borrowed"

    class PydanticMeta:
        exclude = "id"

