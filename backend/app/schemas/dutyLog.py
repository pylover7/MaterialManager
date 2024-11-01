# coding=utf-8
# @FileName  :dutyLog.py
# @Time      :2024/4/10 下午8:31
# @Author    :dayezi
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.dutyLog import DutyLog, DutyNotes

DutyLogPydantic = pydantic_model_creator(DutyLog)
DutyNotesPydantic = pydantic_model_creator(DutyNotes)


class DutyLogCreate(DutyLogPydantic):
    dutyNote_id: int = None


class DutyLogUpdate(DutyLogPydantic):
    ...


class DutyNoteCreate(DutyNotesPydantic):
    ...


class DutyNoteUpdate(DutyNotesPydantic):
    ...


class DutyOverInfo(BaseModel):
    materialData: list[DutyLogCreate]
    materialNote: DutyNoteCreate
    dutyPerson: str
    dutyPersonDepart: str


if __name__ == '__main__':
    from tortoise.contrib.pydantic import pydantic_model_creator
    from app.models.dutyLog import DutyLog, DutyNotes

    DutyLogPydantic = pydantic_model_creator(DutyLog)
    DutyNotesPydantic = pydantic_model_creator(DutyNotes)
    print(DutyLogPydantic.schema(), DutyNotesPydantic.schema())
