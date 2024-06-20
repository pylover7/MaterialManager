# coding=utf-8
# @FileName  :checked.py
# @Time      :2024/6/20 下午10:26
# @Author    :dayezi
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Checked

CheckedPydantic = pydantic_model_creator(Checked)


class CheckedCreate(CheckedPydantic):

    def create_dict(self):
        return self.model_dump(exclude={"id", "created_at", "updated_at"})


class CheckedUpdate(CheckedPydantic):

    def update_dict(self):
        return self.model_dump(exclude={"id", "created_at", "updated_at"})


class ReturnChecked(BaseModel):
    id: int
    returnStatus: bool
    returnUserId: int
