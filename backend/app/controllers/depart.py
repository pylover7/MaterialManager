# coding=utf-8
# @FileName  :depart.py
# @Time      :2024/4/22 上午11:34
# @Author    :dayezi
from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError
from fastapi.exceptions import HTTPException

from app.core.crud import CRUDBase, CreateSchemaType, ModelType
from app.models.users import Depart, User
from app.schemas.users import DepartCreate, DepartUpdate
from app.log import logger


class DepartController(CRUDBase[Depart, DepartCreate, DepartUpdate]):
    def __init__(self):
        super().__init__(model=Depart)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj = await super().create(obj_in)
            return obj
        except IntegrityError:
            raise HTTPException(status_code=406, detail="部门名称已存在！")

    async def get_by_name(self, name: str) -> ModelType:
        q = Q(name=name)
        return await self.model.filter(q).all().first()

    async def get_all_name(self, user: User):
        departAllName = ""
        try:
            depart_id = await user.depart.all().values_list("id", flat=True)
            depart = await self.model.get(id=depart_id)
            departAllName = depart.name + departAllName
            while depart.parentId != 0:
                depart = await self.model.get(id=depart.parentId)
                departAllName = depart.name + departAllName
        except Exception as e:
            logger.error(f"获取部门名称失败: {e}")
        return departAllName


departController = DepartController()
