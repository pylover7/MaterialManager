# coding=utf-8
# @FileName  :dutyLog.py
# @Time      :2024/4/10 下午8:43
# @Author    :dayezi
from typing import List

from app.core.crud import CRUDBase
from app.models.dutyLog import DutyLog, DutyNotes
from app.schemas.dutyLog import DutyLogCreate, DutyLogUpdate, DutyNoteCreate, DutyNoteUpdate


class DutyLogController(CRUDBase[DutyLog, DutyLogCreate, DutyLogUpdate]):
    def __init__(self):
        super().__init__(DutyLog)

    async def create_all(self, data: List[DutyLogCreate]):
        for log in data:
            await self.create(log)


class DutyNotesController(CRUDBase[DutyNotes, DutyNoteCreate, DutyNoteUpdate]):
    def __init__(self):
        super().__init__(DutyNotes)


dutyLogController = DutyLogController()
dutyNotesController = DutyNotesController()
