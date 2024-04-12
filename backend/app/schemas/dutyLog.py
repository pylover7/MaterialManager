# coding=utf-8
# @FileName  :dutyLog.py
# @Time      :2024/4/10 下午8:31
# @Author    :dayezi
from typing import Optional, List

from pydantic import BaseModel, Field


class DutyLog(BaseModel):
    position: str = Field(description="位置")
    name: str = Field(description="名称")
    model: str = Field(description="型号")
    number: str = Field(description="数量")
    nowNumber: int = Field(description="当前数量")
    dutyPerson: str = Field(description="当班人员")
    dutyPersonDepart: str = Field(description="当班人员部门")
    depart: str = Field(description="部门")
    dutyDate: str = Field(description="交班时间")


class DutyLogCreate(DutyLog):

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class DutyLogUpdate(DutyLog):

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class DutyOverInfo(BaseModel):
    materialData: List[DutyLog]
    materialNote: str
    dutyPerson: str
    dutyPersonDepart: str
