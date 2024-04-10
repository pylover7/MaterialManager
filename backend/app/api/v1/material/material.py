import logging

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.controllers.material import GlbMaterialController
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.menus import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/glb_list", summary="查看隔离办物资列表")
async def get_glb_list(
  page: int = Query(1, description="页码"),
  page_size: int = Query(100, description="每页数量"),
  name: str = Query("", description="物资名称")
):
    controller = GlbMaterialController()
    q = Q()
    if name:
      q &= Q(name__contains=name)
    
    total, material_objs = await controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="数据获取成功", data=data, total=total, page=page, page_size=page_size)