# coding=utf-8
# @FileName  :dutyLog.py
# @Time      :2024/4/10 下午8:15
# @Author    :dayezi

from tortoise import fields

from .base import BaseModel


class DutyLog(BaseModel):
    """
    值班日志
    """
    type = fields.CharField(max_length=20, description="物资类型")
    area = fields.CharField(max_length=20, null=False, description="物资所在区域")
    name = fields.CharField(max_length=50, null=False, description="名称")
    position = fields.CharField(max_length=20, null=False, description="位置")
    model = fields.CharField(max_length=20, null=False, description="型号")
    number = fields.IntField(max_length=20, null=False, description="数量")
    nowNumber = fields.IntField(max_length=20, null=False, description="当前数量")
    dutyPerson = fields.CharField(
        max_length=20, null=False, description="当班人员")
    dutyPersonDepart = fields.CharField(
        max_length=20, null=False, description="当班人员部门")
    dutyDate = fields.DatetimeField(auto_now_add=True, description="交班时间")
    dutyNote: fields.ForeignKeyRelation["DutyNotes"] = fields.ForeignKeyField("models.DutyNotes",
                                                                              related_name="duty_log", null=True)

    class Meta:
        table = "dutyLogs"

    class PydanticMeta:
        exclude = ("id", "dutyDate")


class DutyNotes(BaseModel):
    """值班日志备注"""
    note = fields.CharField(max_length=510, null=False, description="备注")
    type = fields.CharField(max_length=20, null=False, description="类型")
    area = fields.CharField(max_length=20, null=False, description="区域")
    dutyDate = fields.DatetimeField(auto_now_add=True, description="交班时间")
    dutyLog: fields.ReverseRelation["DutyLog"]

    class Meta:
        table = "dutyNotes"

    class PydanticMeta:
        exclude = ("id", "dutyDate")
