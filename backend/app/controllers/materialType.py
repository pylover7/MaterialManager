# coding=utf-8
# @FileName  :materialType.py
# @Time      :2024/6/7 下午3:30
# @Author    :dayezi
from app.core.crud import CRUDBase

from app.models import MaterialType
from app.schemas.materialType import MaterialTypeCreate, MaterialTypeUpdate


class MaterialTypeController(CRUDBase[MaterialType, MaterialTypeCreate, MaterialTypeUpdate]):
    def __init__(self):
        super().__init__(model=MaterialType)


materialTypeController = MaterialTypeController()
