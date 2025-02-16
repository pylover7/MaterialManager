from fastapi import APIRouter, Query

from app.controllers.menu import menu_controller
from app.schemas.base import Fail, Success
from app.schemas.menus import *
from app.utils.log import logger

menuRouter = APIRouter()


@menuRouter.post("/add", summary="创建菜单")
async def create_menu(
        data: MenuCreate,
):
    await menu_controller.create(obj_in=data)
    return Success(msg="菜单新增成功")


@menuRouter.delete("/delete", summary="删除菜单")
async def delete_menu(
        id: int = Query(..., description="菜单id"),
        name: str = Query(..., description="菜单名称"),
):
    child_menu_count = await menu_controller.model.filter(parentId=id).count()
    if child_menu_count > 0:
        return Fail(msg="Cannot delete a menu with child menus")
    await menu_controller.remove(id=id)
    logger.info(f"删除菜单【{name}】成功")
    return Success(msg="Deleted Success")


@menuRouter.get("/get", summary="查看单个菜单")
async def get_menu(
        menu_id: int = Query(..., description="菜单id"),
):
    result = await menu_controller.get(id=menu_id)
    return Success(data=result)


@menuRouter.get("/list", summary="查看菜单列表")
async def menu_list():
    _, menus_objs = await menu_controller.list(page=1, page_size=100)
    menu = [await obj.to_dict() for obj in menus_objs]
    return Success(data=menu)


@menuRouter.get("/tree", summary="查看菜单树")
async def menu_tree():
    parent_menus = await menu_controller.model.filter(parent_id=0).order_by("rank")
    res_menu = []
    for menu in parent_menus:
        child_menu = await menu_controller.model.filter(parent_id=menu.id).order_by("rank")
        menu_dict = await menu.to_dict()
        menu_dict["children"] = [await obj.to_dict() for obj in child_menu]
        res_menu.append(menu_dict)
    return Success(data=res_menu)


@menuRouter.post("/update", summary="更新菜单")
async def update_menu(
    menu_in: MenuUpdate,
):
    await menu_controller.update(id=menu_in.id, obj_in=menu_in.update_dict())
    return Success(msg=f"菜单【{menu_in.name}】更新成功")

