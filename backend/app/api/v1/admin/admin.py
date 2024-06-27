# coding=utf-8
# @FileName  :users.py
# @Time      :2024/4/16 下午9:31
# @Author    :dayezi
from typing import Union

from fastapi import APIRouter, Request, Query
from tortoise.expressions import Q, F

from app.controllers import user_controller
from app.controllers.checked import checkedController
from app.controllers.depart import departController
from app.controllers.dutyLog import dutyLogController, dutyNotesController
from app.models import Checked
from app.schemas.checked import ReturnChecked, CheckedCreate
from app.settings import settings
from app.core.init_db import test_db, set_db
from app.log import logger
from app.schemas import Success, Fail, SuccessExtra
from app.schemas.admin import DbInfo
from app.utils import now

router = APIRouter()


@router.get("/get_db_info")
async def get_db_info():
    data = settings.DATABASE_INFO.model_dump()
    return Success(data=data)


@router.post("/test_db_info", summary="测试数据库连接")
async def test_db_conn(data: DbInfo):
    if test_db(data):
        return Success(msg="数据库链接成功！")
    else:
        return Fail(msg="数据库链接失败！")


@router.post("/set_db_info", summary="设置数据库连接")
async def set_db_conn(data: DbInfo, request: Request):
    try:
        await set_db(data, request.app)
        return Success(msg="数据库设置成功！")
    except Exception as e:
        logger.error(e)
        return Fail(msg="数据库设置失败！")


@router.post("/dutyLogs/search", summary="查询操作日志")
async def search_operation_logs(
        data: dict,
        area: str = Query("glb", description="区域"),
        metaType: str = Query("tool", description="工具类型"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
):
    q = Q(Q(area__contains=area), Q(type__contains=metaType))
    status = data.get("status")
    operatingTime: list = data.get("operatingTime")
    if status:
        # 数据库字段条件筛选：字段是否相等
        if int(status) == 1:
            q &= Q(number=F("nowNumber"))
        else:
            q &= Q(number__not=F("nowNumber"))
    if len(operatingTime) > 1:
        # 数据库字段条件筛选：大小比较
        q &= Q(dutyDate__gte=operatingTime[0], dutyDate__lte=operatingTime[1])
    total, duty_logs = await dutyLogController.list(page=page, page_size=pageSize, search=q)
    data = [await obj.to_dict() for obj in duty_logs]
    return SuccessExtra(data=data, total=total, currentPage=page, pageSize=pageSize)


@router.delete("/dutyLogs/delete", summary="批量删除操作日志")
async def delete_operation_logs(data: list[int]):
    for item in data:
        await dutyLogController.remove(item)
    return Success(msg="操作日志删除成功！")


@router.get("/getDutyNote", summary="获取值班备注")
async def get_duty_note(id: int = Query(..., description="值班备注id")):
    data = await dutyNotesController.get(id)
    data = await data.to_dict()
    return Success(data=data)


@router.get("/getChecked", summary="获取物资送检信息")
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
        userDepart = await departController.get_all_name(user)
        material = await obj.material.all()
        material_dict = await material.to_dict()
        user_dict = await user.to_dict()
        user_dict["depart"] = userDepart
        obj_dict = await obj.to_dict()
        obj_dict["material"] = material_dict
        obj_dict["toCheckUser"] = user_dict
        try:
            user2 = await obj.toReturnUser.all()
            user2Depart = await departController.get_all_name(user2)
            user_dict2 = await user2.to_dict()
            obj_dict["toReturnUser"] = user_dict2
            user_dict2["depart"] = user2Depart
        except Exception as e:
            logger.warning(f"物资【{material.name}】暂无归还人信息：{e}")
        data.append(obj_dict)
    return SuccessExtra(data=data, total=total, currentPage=page, pageSize=pageSize)


@router.post("/updateChecked", summary="归还送检物资")
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


@router.post("/createChecked", summary="创建物资送检信息")
async def create_checked(data: dict):
    user = await user_controller.get_by_uuid(data.get("toCheckUserUUID"))
    data["toCheckUser"] = user
    obj: Checked = await checkedController.create(obj_in=data)
    material = await obj.material.all()
    material.checking += obj.number
    await material.save()
    return Success(data=await obj.to_dict(m2m=True))


@router.get("/deleteChecked", summary="删除物资送检信息")
async def delete_checked(data: list[int]):
    for id in data:
        await checkedController.remove(id)
    return Success(msg="删除成功！")
