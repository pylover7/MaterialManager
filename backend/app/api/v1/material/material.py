from typing import Union

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.material import materialController
from app.models import Material
from app.schemas.base import Success, SuccessExtra, Fail
from app.schemas.material import MaterialCreate, MaterialUpdate
from app.utils import generate_uuid
from app.utils.log import logger


router = APIRouter()


@router.get("/meta", summary="获取物资源数据")
async def get_meta(
        area: str = Query("glb", description="物资区域"),
        metaType: str = Query("", description="物资类型"),
        page: int = Query(1, description="页码"),
        pageSize: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称"),
):
    q = Q(Q(area__contains=area), Q(type__contains=metaType))
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await materialController.list(page=page, page_size=pageSize, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="物资数据获取成功", data=data, total=total, page=page, pageSize=pageSize)


@router.get("/allMeta", summary="获取所有物资源数据")
async def get_all_meta(
        area: str = Query("glb", description="物资区域"),
        metaType: str = Query("tool", description="物资类型")
):
    q = Q(Q(area__contains=area), Q(type__contains=metaType))
    material_objs = await materialController.all(search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return Success(data=data)


@router.post("/addMeta", summary="添加或修改物资源数据")
async def add_meta(data: Union[MaterialCreate, MaterialUpdate]):
    if hasattr(data, "id"):
        result: Material = await materialController.update(data.id, data)
    else:
        data: dict = data.model_dump()
        data["uuid"] = generate_uuid(data["name"])
        result: Material = await materialController.create(data)
    result = await result.to_dict()
    if result:
        return Success(data=result)
    else:
        return Fail(msg="数据写入失败！")


@router.delete("/delete", summary="删除物资源数据")
async def delete_meta(data: dict[str, list[int]]):
    for id in data["idList"]:
        try:
            await materialController.remove(id)
        except Exception as e:
            logger.error(f"删除物资项失败，ID为{id}")
            return Fail(msg=f"删除物资项部分失败: {e}")
    return Success(msg="删除成功")
