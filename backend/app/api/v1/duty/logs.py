# coding=utf-8
# @FileName  :logs.py
# @Time      :2024/7/6 上午3:58
# @Author    :dayezi
from tortoise.expressions import Q, F
from fastapi import Query, APIRouter

from app.controllers.dutyLog import dutyLogController
from app.schemas import Success, SuccessExtra

logRouter = APIRouter()


@logRouter.post("/list", summary="查询值班日志")
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


@logRouter.delete("/delete", summary="删除值班日志")
async def delete_operation_logs(data: list[int]):
    for item in data:
        await dutyLogController.remove(item)
    return Success(msg="操作日志删除成功！")
