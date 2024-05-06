from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.controllers import role_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.roles import *
from app.log import logger


router = APIRouter()


@router.post("/list", summary="条件查询角色列表")
async def list_role(
        data: RoleFilter,
        currentPage: int = Query(1, description="页码"),
        pageSize: int = Query(100, description="每页数量"),
):
    q = Q()
    if data.name:
        q = q & Q(name__contains=data.name)
    if data.code:
        q = q & Q(code__contains=data.code)
    if isinstance(data.status, int):
        q = q & Q(status__contains=data.status)
    total, role_objs = await role_controller.list(page=currentPage, page_size=pageSize, search=q)
    data = [await obj.to_dict() for obj in role_objs]
    return SuccessExtra(data=data, total=total, currentPage=currentPage, pageSize=pageSize)


@router.get("/get", summary="查看角色")
async def get_role(
        id: int = Query(..., description="角色ID"),
):
    role_obj = await role_controller.get(id=id)
    return Success(data=await role_obj.to_dict())


@router.post("/add", summary="新增角色")
async def create_role(data: RoleCreate):
    if await role_controller.is_exist(name=data.name):
        raise HTTPException(
            status_code=400,
            detail="该角色名已存在！",
        )
    result = await role_controller.create(obj_in=data)
    result = await result.to_dict()
    return Success(msg="创建成功！", data=result)


@router.post("/update", summary="更新角色")
async def update_role(role_in: RoleUpdate):
    result = await role_controller.update(id=role_in.id, obj_in=role_in.update_dict())
    result = await result.to_dict()
    return Success(msg="更新成功", data=result)


@router.delete("/delete", summary="删除角色")
async def delete_role(
    id: int = Query(..., description="角色ID"),
    name: str = Query(..., description="角色名称"),
):
    await role_controller.remove(id=id)
    logger.info(f"删除角色: {name}")
    return Success(msg="Deleted Success")


@router.get("/getRoleAuth", summary="查看角色权限")
async def get_role_menu_id(id: int = Query(..., description="角色ID")):
    role_obj = await role_controller.get(id=id)
    menuID = await role_obj.menus.all().values_list("id", flat=True)
    apiId = await role_obj.apis.all().values_list("id", flat=True)
    data = {
        "menus": menuID,
        "apis": apiId
    }
    return Success(data=data)


@router.post("/updateRoleAuth", summary="更新角色权限")
async def update_role_menu_id(data: RoleUpdateMenusApis):
    role_obj = await role_controller.get(id=data.id)
    await role_controller.update_roles(role=role_obj, menu_ids=data.menus, api_ids=data.apis)
    return Success(msg="权限更新成功")

