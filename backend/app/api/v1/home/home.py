# coding=utf-8
# @FileName  :home.py
# @Time      :2024/5/31 上午7:15
# @Author    :dayezi
from fastapi import APIRouter, Query
from tortoise.expressions import Q
from app.controllers.borrowed import borrowedController
from app.controllers.material import materialController
from app.models import Borrowed
from app.schemas import Success, SuccessExtra
from app.schemas.borrowed import CreateBorrowedInfo

router = APIRouter()


@router.get("/list", summary="获取全部借用信息")
async def get_home_list(
        area: str = Query("glb", description="区域"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量")
):
    q = Q(material__depart=area)
    total, objs = await borrowedController.list(page=page, page_size=pageSize, search=q)
    data = [await obj.to_dict(m2m=True) for obj in objs]
    return SuccessExtra(data=data, total=total, currentPage=page, pageSize=pageSize)


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
