# coding=utf-8
# @FileName  :checked.py
# @Time      :2024/7/6 下午7:05
# @Author    :dayezi
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers import user_controller
from app.controllers.checked import checkedController
from app.models import Checked
from app.schemas.checked import ReturnChecked
from app.log import logger
from app.schemas import Success, SuccessExtra
from app.utils import now

checkedRouter = APIRouter()


@checkedRouter.post("/add", summary="新增物资送检信息")
async def create_checked(data: dict):
    user = await user_controller.get_by_uuid(data.get("toCheckUserUUID"))
    data["toCheckUser"] = user
    obj: Checked = await checkedController.create(obj_in=data)
    material = await obj.material.all()
    material.checking += obj.number
    await material.save()
    return Success(data=await obj.to_dict(m2m=True))


@checkedRouter.delete("/delete", summary="删除物资送检信息")
async def delete_checked(data: list[int]):
    for id in data:
        await checkedController.remove(id)
    return Success(msg="删除成功！")


@checkedRouter.get("/get", summary="获取物资送检信息")
async def get_checked(
        area: str = Query("glb", description="区域"),
        metaType: str = Query("tool", description="工具类型"),
        returnStatus: bool = Query(False, description="归还状态"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
):
    q = Q(area__contains=area) & Q(type__contains=metaType) & Q(returnStatus=returnStatus)
    total, checked_objs = await checkedController.list(page=page, page_size=pageSize, search=q)
    data = []
    for obj in checked_objs:
        user = await obj.toCheckUser.all()
        userDepart = user.department
        material = await obj.material.all()
        material_dict = await material.to_dict()
        user_dict = await user.to_dict()
        user_dict["depart"] = userDepart
        obj_dict = await obj.to_dict()
        obj_dict["material"] = material_dict
        obj_dict["toCheckUser"] = user_dict
        try:
            user2 = await obj.toReturnUser.all()
            user2Depart = user2.department
            user_dict2 = await user2.to_dict()
            obj_dict["toReturnUser"] = user_dict2
            user_dict2["depart"] = user2Depart
        except Exception as e:
            logger.warning(f"物资【{material.name}】暂无归还人信息：{e}")
        data.append(obj_dict)
    return SuccessExtra(data=data, total=total, currentPage=page, pageSize=pageSize)


@checkedRouter.post("/update", summary="归还送检物资")
async def update_checked(data: ReturnChecked):
    user = await user_controller.get_by_uuid(data.toReturnUserUUID)
    for id in data.idList:
        obj: Checked = await checkedController.get(id=id)
        material = await obj.material.all()
        material.checking -= obj.number
        await material.save()
        obj.toReturnUser = user
        obj.returnStatus = True
        obj.note = data.note
        obj.returnDate = now()
        await obj.save()
    return Success(msg="更新成功！")

