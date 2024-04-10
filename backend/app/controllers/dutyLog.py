# coding=utf-8
# @FileName  :dutyLog.py
# @Time      :2024/4/10 下午8:43
# @Author    :dayezi
from typing import List

from app.core.crud import CRUDBase
from app.models.dutyLog import DutyLog
from app.schemas.dutyLog import DutyLogCreate, DutyLogUpdate


class DutyLogController(CRUDBase[DutyLog, DutyLogCreate, DutyLogUpdate]):
    def __init__(self):
        super().__init__(DutyLog)

    async def create_all(self, data: List[DutyLogCreate]):
        for log in data:
            await self.create(log)


dutyLogController = DutyLogController()
