# coding=utf-8
# @FileName  :checked.py
# @Time      :2024/6/20 下午10:29
# @Author    :dayezi
from app.core.crud import CRUDBase
from app.models import Checked
from app.schemas.checked import CheckedCreate, CheckedUpdate


class CheckedController(CRUDBase[Checked, CheckedCreate, CheckedUpdate]):
    def __init__(self):
        super().__init__(model=Checked)


checkedController = CheckedController()
