# coding=utf-8
# @FileName  :borrowed.py
# @Time      :2024/5/31 上午12:49
# @Author    :dayezi
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.borrowed import Borrowed
from app.schemas.material import MaterialCreate

BorrowedPydantic = pydantic_model_creator(Borrowed)


class BorrowedCreate(BorrowedPydantic):

    def create_dict(self):
        return self.model_dump(exclude={"id", "borrowApproveUser", "returnApproveUser"})


class BorrowedUpdate(BorrowedPydantic):

    def update_dict(self):
        return self.model_dump(exclude={"id", "borrowApproveUser", "returnApproveUser"})


class MaterialBorrowed(MaterialCreate):
    uuid: str
    borrowing: int


class CreateBorrowedInfo(BaseModel):
    uuid: str
    username: str
    nickname: str
    phone: str
    depart: str
    reason: str
    baseData: list[MaterialBorrowed]


class UpdateBorrowedInfo(BaseModel):
    uuid: str
    idList: list[int]
    borrowStatus: bool = None
    borrowWhether: bool = None
    returnStatus: bool = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "uuid": "uuid",
                "idList": [1, 2, 3],
                "status": True
            }
        }
