import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.material import MaterialController, MaterialNoteController
from app.schemas.base import Fail, Success, SuccessExtra

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/glb_list", summary="获取隔离办物资列表")
async def get_glb_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称"),
):
    controller = MaterialController()
    q = Q(depart__contains="glb")
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="隔离办数据获取成功", data=data, total=total, page=page, page_size=page_size)


@router.get("/glb_note", summary="获取隔离办物资注意事项")
async def get_glb_note():
    controller = MaterialNoteController()
    q = Q(depart__contains="glb")
    total, note_objs = await controller.list(page=1, page_size=100, search=q)
    data = [await obj.to_dict() for obj in note_objs]
    return Success(msg="隔离办注意事项", data=data)


@router.get("/fk_material", summary="查看辅控物资列表")
async def get_fk_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称")
):
    controller = MaterialController()
    q = Q(depart__contains="fk")
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="辅控数据获取成功", data=data, total=total, page=page, page_size=page_size)


@router.get("/wk_material", summary="查看网控物资列表")
async def get_fk_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称")
):
    controller = MaterialController()
    q = Q(depart__contains="wk")
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="网控数据获取成功", data=data, total=total, page=page, page_size=page_size)
