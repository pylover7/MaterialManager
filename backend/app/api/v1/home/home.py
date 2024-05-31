# coding=utf-8
# @FileName  :home.py
# @Time      :2024/5/31 上午7:15
# @Author    :dayezi
from fastapi import APIRouter
from app.controllers.borrowed import borrowedController
from app.controllers.material import materialController
from app.models import Borrowed
from app.schemas import Success
from app.schemas.borrowed import CreateBorrowedInfo

router = APIRouter()


@router.get("/list_all", summary="获取全部借用信息")
async def get_home_list():
    objs = await borrowedController.all()
    data = [await obj.to_dict() for obj in objs]
    return Success(data=data)


@router.post("/create", summary="创建借用信息")
async def create_borrowed(data: CreateBorrowedInfo):
    for item in data.baseData:
        # 前端发送的uuid为物资的uuid，这里在查询完毕后，使用用户的uuid将其代替
        material = await materialController.get_by_uuid(uuid=item.uuid)
        item = item.model_dump()
        item["username"] = data.username
        item["phone"] = data.phone
        item["userDepart"] = data.depart
        item["uuid"] = data.uuid
        obj: Borrowed = await borrowedController.create(obj_in=item)
        await obj.material.add(material)
    return Success()

