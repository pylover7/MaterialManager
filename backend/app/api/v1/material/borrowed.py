# coding=utf-8
# @FileName  :borrowed.py
# @Time      :2024/7/6 下午7:37
# @Author    :dayezi
# coding=utf-8
# @FileName  :home.py
# @Time      :2024/5/31 上午7:15
# @Author    :dayezi
from fastapi import APIRouter, Query
from tortoise.expressions import Q
from typing import Union

from app.controllers import user_controller
from app.controllers.borrowed import borrowedController
from app.controllers.depart import departController
from app.controllers.material import materialController
from app.models import Borrowed
from app.schemas import Success, SuccessExtra
from app.schemas.borrowed import CreateBorrowedInfo, UpdateBorrowedInfo
from app.utils import now

borrowedRouter = APIRouter()


@borrowedRouter.post("/add", summary="创建借用信息")
async def create_borrowed(data: CreateBorrowedInfo):
    for item in data.baseData:
        # 前端发送的uuid为物资的uuid，这里在查询完毕后，使用用户的uuid将其代替
        material = await materialController.get_by_uuid(uuid=item.uuid)
        item = item.model_dump()
        item["username"] = data.username
        item["nickname"] = data.nickname
        item["phone"] = data.phone
        item["userDepart"] = data.depart
        item["uuid"] = data.uuid
        user = await user_controller.get_by_uuid(item["uuid"])
        item["phone"] = user.phone
        item["reason"] = data.reason
        item["material_id"] = material.id
        obj: Borrowed = await borrowedController.create(obj_in=item)
        material.borrowed += obj.borrowing
        await material.save()
    return Success()


@borrowedRouter.post("/delete", summary="删除借用信息")
async def delete_borrowed(data: dict):
    for id in data["idList"]:
        obj = await borrowedController.get(id=id)
        await obj.delete()
    return Success()


@borrowedRouter.get("/list", summary="获取借用信息")
async def get_home_list(
        area: str = Query("glb", description="区域"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
        borrowedStatus: Union[bool, None] = Query(None, description="借用批准状态"),
        borrowWhether: Union[bool, None] = Query(None, description="借用通过状态"),
        returnStatus: Union[bool, None] = Query(None, description="归还批准状态")
):
    q = Q(material__area=area)
    if borrowedStatus is not None:
        q &= Q(borrowApproveStatus=borrowedStatus)
    if borrowWhether is not None:
        q &= Q(Q(borrowApproveWhether=borrowWhether), Q(returnApproveStatus=returnStatus))
    total, objs = await borrowedController.list(page=page, page_size=pageSize, search=q)
    data = []
    for obj in objs:
        material = await obj.material.all().values("name", "model", "position", "number", "borrowed")
        obj_dict = await obj.to_dict()
        if obj.borrowApproveStatus:
            borrowApproveUser = await obj.borrowApproveUser.all().values("id", "username", "phone", "depart_id")
            user = await user_controller.get(borrowApproveUser["id"])
            depart = await departController.get_all_name(user)
            borrowApproveUser["depart"] = depart
            obj_dict["borrowApproveUser"] = borrowApproveUser
        if obj.returnApproveStatus:
            returnApproveUser = await obj.returnApproveUser.all().values("id", "username", "phone", "depart_id")
            user = await user_controller.get(returnApproveUser["id"])
            depart = await departController.get_all_name(user)
            returnApproveUser["depart"] = depart
            obj_dict["returnApproveUser"] = returnApproveUser
        obj_dict["material"] = material
        data.append(obj_dict)
    return SuccessExtra(data=data, total=total, currentPage=page, pageSize=pageSize)


@borrowedRouter.post("/update", summary="更新借用信息")
async def update_borrowed(data: UpdateBorrowedInfo):
    uuid = data.uuid
    user = await user_controller.get_by_uuid(uuid)

    for id in data.idList:
        obj = await borrowedController.get(id=id)
        if data.borrowStatus:
            obj.borrowApproveUser_id = user.id
            obj.borrowApproveStatus = data.borrowStatus
            obj.borrowApproveWhether = data.borrowWhether
            obj.borrowApproveTime = now(0)
        elif data.returnStatus:
            obj.returnApproveUser_id = user.id
            obj.returnApproveStatus = data.returnStatus
            obj.returnApproveTime = now(0)
        if not data.borrowWhether or data.returnStatus:
            material_id = obj.material_id
            material = await materialController.get(id=material_id)
            material.borrowed -= obj.borrowing
            await material.save()

        await obj.save()
    return Success()

