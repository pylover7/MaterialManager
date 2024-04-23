# coding=utf-8
# @FileName  :depart.py
# @Time      :2024/4/22 上午11:34
# @Author    :dayezi
from tortoise.exceptions import IntegrityError
from fastapi.exceptions import HTTPException

from app.core.crud import CRUDBase, CreateSchemaType, ModelType
from app.models.users import Depart
from app.schemas.users import DepartCreate, DepartUpdate


class DepartController(CRUDBase[Depart, DepartCreate, DepartUpdate]):
    def __init__(self):
        super().__init__(model=Depart)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj = await super().create(obj_in)
            return obj
        except IntegrityError:
            raise HTTPException(status_code=403, detail="部门名称已存在！")


departController = DepartController()
