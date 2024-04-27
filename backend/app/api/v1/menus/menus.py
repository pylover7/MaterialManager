import logging

from fastapi import APIRouter, Query

from app.controllers.menu import menu_controller
from app.schemas.base import Fail, Success, SuccessExtra
from app.schemas.menus import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/tree", summary="查看菜单树")
async def menu_tree():
    parent_menus = await menu_controller.model.filter(parent_id=0).order_by("order")
    res_menu = []
    for menu in parent_menus:
        child_menu = await menu_controller.model.filter(parent_id=menu.id).order_by("order")
        menu_dict = await menu.to_dict()
        menu_dict["children"] = [await obj.to_dict() for obj in child_menu]
        res_menu.append(menu_dict)
    return Success(data=res_menu)


@router.get("/list", summary="查看菜单列表")
async def menu_list():
    _, menus_objs = await menu_controller.list(page=1, page_size=1000)
    menu = [await obj.to_dict() for obj in menus_objs]
    return Success(data=menu)


@router.get("/get", summary="查看单个菜单")
async def get_menu(
        menu_id: int = Query(..., description="菜单id"),
):
    result = await menu_controller.get(id=menu_id)
    return Success(data=result)


@router.post("/add", summary="创建菜单")
async def create_menu(
        data: MenuCreate,
):
    await menu_controller.create(obj_in=data)
    return Success(msg="菜单新增成功")


@router.post("/update", summary="更新菜单")
async def update_menu(
    menu_in: MenuUpdate,
):
    await menu_controller.update(id=menu_in.id, obj_in=menu_in.update_dict())
    return Success(msg="Updated Success")


@router.delete("/delete", summary="删除菜单")
async def delete_menu(
        id: int = Query(..., description="菜单id"),
):
    child_menu_count = await menu_controller.model.filter(parent_id=id).count()
    if child_menu_count > 0:
        return Fail(msg="Cannot delete a menu with child menus")
    await menu_controller.remove(id=id)
    return Success(msg="Deleted Success")
