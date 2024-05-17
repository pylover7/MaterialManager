# coding=utf-8
# @FileName  :users.py
# @Time      :2024/4/16 下午9:31
# @Author    :dayezi
from fastapi import APIRouter, Request, Query
from tortoise.expressions import Q, F

from app.controllers.dutyLog import dutyLogController, dutyNotesController
from app.settings import settings
from app.core.init_db import test_db, set_db
from app.log import logger
from app.schemas import Success, Fail, SuccessExtra
from app.schemas.admin import DbInfo

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
        depart: str = Query("glb", description="部门"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
):
    q = Q(depart__contains=depart)
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
