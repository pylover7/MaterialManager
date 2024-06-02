# coding=utf-8
# @FileName  :borrowed.py
# @Time      :2024/5/31 上午12:55
# @Author    :dayezi
from app.core.crud import CRUDBase
from app.models.borrowed import Borrowed
from app.schemas.borrowed import BorrowedCreate, BorrowedUpdate


class BorrowedController(CRUDBase[Borrowed, BorrowedCreate, BorrowedUpdate]):
    def __init__(self):
        super().__init__(model=Borrowed)


borrowedController = BorrowedController()
