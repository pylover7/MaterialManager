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


@router.post("/add", summary="添加部门")
async def add_depart(data: DepartCreate):
    result = await departController.create(data)
    data = await result.to_dict()
    logger.success(f"部门添加成功！{data}")
    return Success(msg="部门添加成功！", data=data)


@router.get("/list", summary="部门列表")
async def depart_list():
    _, depart_obj = await departController.list(1, 1000)
    data = [await obj.to_dict() for obj in depart_obj]
    logger.success(f"部门列表查询成功！{[i['name'] for i in data]}")
    return Success(msg="部门列表查询成功！", data=data)
