# coding=utf-8
# @FileName  :home.py
# @Time      :2024/5/31 上午7:15
# @Author    :dayezi
from fastapi import APIRouter, Query
from tortoise.expressions import Q
from typing import Union

from app.controllers import user_controller
from app.controllers.borrowed import borrowedController
from app.controllers.material import materialController
from app.models import Borrowed
from app.schemas import Success, SuccessExtra
from app.schemas.borrowed import CreateBorrowedInfo, UpdateBorrowedInfo
from app.utils import now

router = APIRouter()


@router.get("/list", summary="获取借用信息")
async def get_home_list(
        area: str = Query("glb", description="区域"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
        borrowedStatus: bool = Query(False, description="借用批准状态"),
        borrowWhether: Union[bool, None] = Query(None, description="借用通过状态"),
        returnStatus: Union[bool, None] = Query(None, description="归还批准状态")
):
    if returnStatus is None:
        q = Q(Q(material__depart=area), Q(borrowApproveStatus=borrowedStatus))
    else:
        q = Q(Q(material__depart=area), Q(borrowApproveWhether=borrowWhether), Q(returnApproveStatus=returnStatus))
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
        material.borrowed += obj.borrowing
        await material.save()
        await obj.material.add(material)
    return Success()


@router.post("/update", summary="更新借用信息")
async def update_borrowed(data: UpdateBorrowedInfo):
    uuid = data.uuid
    user = await user_controller.get_by_uuid(uuid)

    for id in data.idList:
        obj = await borrowedController.get(id=id)
        if data.borrowStatus:
            await obj.borrowApproveUser.add(user)
            obj.borrowApproveStatus = data.borrowStatus
            obj.borrowApproveWhether = data.borrowWhether
            obj.borrowApproveTime = now(False)
        elif data.returnStatus:
            await obj.returnApproveUser.add(user)
            obj.returnApproveStatus = data.returnStatus
            obj.returnApproveTime = now(False)
        if not data.borrowWhether or data.returnStatus:
            material_id = await obj.material.all().values_list("id", flat=True)
            material = await materialController.get(id=material_id[0])
            material.borrowed -= obj.borrowing
            await material.save()

        await obj.save()
    return Success()


@router.delete("/delete", summary="删除借用信息")
async def delete_borrowed(data: list[int]):
    for id in data:
        obj = await borrowedController.get(id=id)
        await obj.delete()
    return Success()
