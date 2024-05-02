import logging

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.controllers.user import user_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.users import *

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看用户列表")
async def list_user(
    currentPage: int = Query(1, description="页码"),
    pageSize: int = Query(10, description="每页数量"),
    username: str = Query("", description="用户名称，用于搜索"),
    phone: str = Query("", description="手机号码，用于搜索"),
):
    q = Q()
    if username:
        q &= Q(username__contains=username)
    if phone:
        q &= Q(email__contains=phone)
    total, user_objs = await user_controller.list(page=currentPage, page_size=pageSize, search=q)
    data = [await obj.to_dict(m2m=True, exclude_fields=["password"]) for obj in user_objs]
    return SuccessExtra(data=data, total=total, currentPage=currentPage, pageSize=pageSize)


@router.get("/get", summary="查看用户")
async def get_user(
    user_id: int = Query(..., description="用户ID"),
):
    user_obj = await user_controller.get(id=user_id)
    user_dict = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=user_dict)


@router.post("/add", summary="新增用户")
async def create_user(
    data: UserCreate,
):
    user = await user_controller.get_by_username(data.username)
    if user or (data.username == "admin"):
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    id = data.departId
    del data.departId
    new_user = await user_controller.create(obj_in=data)
    await user_controller.update_depart(new_user, id)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新用户")
async def update_user(
    user_in: UserUpdate,
):
    user = await user_controller.update(obj_in=user_in)
    await user_controller.update_roles(user, user_in.roles)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除用户")
async def delete_user(
    user_id: int = Query(..., description="用户ID"),
):
    await user_controller.remove(id=user_id)
    return Success(msg="Deleted Successfully")
