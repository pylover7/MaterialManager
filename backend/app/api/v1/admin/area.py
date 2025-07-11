# coding=utf-8
# @FileName  :area.py
# @Time      :2024/12/3 16:00
# @Author    :dayezi
from fastapi import APIRouter, Query
from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError

from app.controllers.area import areaController
from app.schemas import Success, SuccessExtra, Fail
from app.schemas.area import AreaCreate, AreaUpdate
from app.utils import generate_uuid

areaRouter = APIRouter()


@areaRouter.post("/add", summary="新增区域")
async def create_area(
        data: AreaCreate,
):
    data.uuid = generate_uuid(data.name).__str__()
    try:
        area = await areaController.create(obj_in=data)
    except IntegrityError:
        return Fail(msg="区域名称或编码已存在")
    return Success(data=await area.to_dict())


@areaRouter.delete("/delete", summary="删除区域")
async def delete_area(
        id: int,
):
    await areaController.remove(id)
    return Success(msg="删除成功")


@areaRouter.put("/update", summary="更新区域")
async def update_area(
        data: AreaUpdate,
):
    area = await areaController.update(id=data.id, obj_in=data)
    return Success(data=await area.to_dict())


@areaRouter.get("/updateStatus", summary="修改区域状态")
async def update_area_status(
        id: int = Query(..., description="区域ID"),
        status: int = Query(..., description="状态：启用/停用"),
):
    area = await areaController.update(id=id, obj_in={"status": status})
    return Success(data=await area.to_dict())


@areaRouter.get("/list", summary="查看区域列表")
async def list_area(
        currentPage: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
        name: str = Query("", description="区域名称，用于搜索"),
        code: str = Query("", description="区域编码，用于搜索"),
):
    q = Q()
    if name:
        q &= Q(name__icontains=name)
    if code:
        q &= Q(code__icontains=code)
    total, area_list = await areaController.list(currentPage, pageSize, q)
    data = []
    for area in area_list:
        item = await area.to_dict()
        data.append(item)
    return SuccessExtra(total=total, data=data, msg="查询成功",
                        currentPage=currentPage, pageSize=pageSize)


@areaRouter.get("/all", summary="查看所有区域")
async def list_all_area():
    area_list = await areaController.all()
    data = []
    for area in area_list:
        if area.status == 0:
            continue
        item = await area.to_dict()
        data.append(item)
    return Success(data=data, msg="查询成功")
