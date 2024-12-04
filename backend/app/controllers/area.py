# coding=utf-8
# @FileName  :area.py
# @Time      :2024/6/9 上午9:53
# @Author    :dayezi
from app.core.crud import CRUDBase

from app.models import MaterialArea
from app.schemas.area import AreaCreate, AreaUpdate


class MaterialAreaController(CRUDBase[MaterialArea, AreaCreate, AreaUpdate]):
    def __init__(self):
        super().__init__(model=MaterialArea)


areaController = MaterialAreaController()
