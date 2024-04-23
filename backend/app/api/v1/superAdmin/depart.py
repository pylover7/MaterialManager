# coding=utf-8
# @FileName  :depart.py
# @Time      :2024/4/23 上午2:00
# @Author    :dayezi
from fastapi import APIRouter

from app.settings import settings
from app.controllers.depart import departController
from app.log import logger
from app.schemas import Success, Fail
from app.schemas.users import DepartCreate

router = APIRouter()


@router.post("/add")
async def add_depart(data: DepartCreate):
    result = await departController.create(data)
    data = await result.to_dict()
    logger.success(f"部门添加成功！{data}")
    return Success(msg="部门添加成功！", data=data)
