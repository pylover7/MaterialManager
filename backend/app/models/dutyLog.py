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
    position = fields.CharField(max_length=20, null=False, description="位置")
    name = fields.CharField(max_length=50, null=False, description="名称")
    model = fields.CharField(max_length=20, null=False, description="型号")
    number = fields.CharField(max_length=20, null=False, description="数量")
    nowNumber = fields.IntField(null=False, description="当前数量")
    dutyPerson = fields.CharField(max_length=20, null=False, description="当班人员")
    dutyPersonDepart = fields.CharField(max_length=20, null=False, description="当班人员部门")
    depart = fields.CharField(max_length=20, null=False, description="部门")
    dutyDate = fields.DatetimeField(auto_now_add=True, description="交班时间")
    dutyNote: fields.ForeignKeyRelation["DutyNotes"] = fields.ForeignKeyField("models.DutyNotes",
                                                                              related_name="duty_log")

    class Meta:
        table = "dutyLogs"

    class PydanticMeta:
        exclude = ("dutyDate", "id")


class DutyNotes(BaseModel):
    """值班日志备注"""
    note = fields.CharField(max_length=510, null=False, description="备注")
    depart = fields.CharField(max_length=255, null=False, description="部门")
    dutyDate = fields.DatetimeField(auto_now_add=True, description="交班时间")
    dutyLog: fields.ReverseRelation["DutyLog"]

    class Meta:
        table = "dutyNotes"

    class PydanticMeta:
        exclude = ("dutyLog", "dutyDate", "id")


