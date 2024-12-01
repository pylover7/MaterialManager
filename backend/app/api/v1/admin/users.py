import time
from pathlib import Path

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.controllers.user import user_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.users import *
from app.log import logger
from app.settings import settings
from app.utils import base_decode, generate_uuid
from app.utils.password import get_password_hash

userRouter = APIRouter()


@userRouter.post("/add", summary="新增用户")
async def create_user(
        data: UserCreate,
):
    user = await user_controller.get_by_username(data.username)
    if user or (data.username == "admin"):
        raise HTTPException(
            status_code=400,
            detail="用户已存在",
        )
    id = data.departId
    del data.departId
    data.uuid = generate_uuid(data.username)
    new_user = await user_controller.create(obj_in=data)
    await user_controller.update_depart(new_user, id)
    return Success(msg="Created Successfully")


@userRouter.delete("/delete", summary="删除用户")
async def delete_user(
        id: int = Query(..., description="用户ID"),
        name: str = Query(..., description="用户名称"),
):
    await user_controller.remove(id=id)
    logger.warning(f"用户 {name} 已被删除")
    return Success(msg="Deleted Successfully")


@userRouter.get("/get", summary="查看用户")
async def get_user(
        user_id: int = Query(..., description="用户ID"),
):
    user_obj = await user_controller.get(id=user_id)
    user_dict = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=user_dict)


@userRouter.get("/list", summary="查看用户列表")
async def list_user(
        currentPage: int = Query(1, description="页码"),
        pageSize: int = Query(10, description="每页数量"),
        username: str = Query("", description="工号，用于搜索"),
        nickname: str = Query("", description="用户名称，用于搜索"),
):
    q = Q()
    if username:
        q &= Q(username__contains=username)
    if nickname:
        q &= Q(nickname__contains=nickname)
    total, user_objs = await user_controller.list(page=currentPage, page_size=pageSize, search=q)
    data = []
    for obj in user_objs:
        obj_dict = await obj.to_dict(m2m=True)
        data.append(obj_dict)
    return SuccessExtra(data=data, total=total, currentPage=currentPage, pageSize=pageSize)


@userRouter.post("/update", summary="更新用户")
async def update_user(
        data: UserUpdate,
):
    id = data.departId
    del data.departId
    user = await user_controller.update(obj_in=data)
    await user_controller.update_depart(user, id)
    return Success(msg="Updated Successfully")


@userRouter.post("/updateStatus", summary="更新用户状态")
async def update_status(
        data: UpdateStatus,
):
    user = await user_controller.get(id=data.id)
    await user_controller.update_status(user, data.status)
    return Success(msg="Updated Successfully")


@userRouter.post("/updateAvatar", summary="更新用户头像")
async def update_avatar(
        data: dict,
        id: int = Query(..., description="用户ID"),
):
    user = await user_controller.get(id=id)
    avatar_name = f"{user.uuid}_{time.time_ns()}.{data['base64'].split(';')[0].split('/')[-1]}"
    avatar_path = Path.joinpath(settings.STATIC_PATH, "avatar", avatar_name)
    with open(avatar_path, "wb") as f:
        imgData = base_decode(data["base64"].split(",")[1])
        f.write(imgData)
    user.avatar = avatar_name
    await user.save()
    return Success(msg="Updated Successfully")


@userRouter.post("/updateRoles", summary="更新用户角色")
async def update_roles(
        data: dict,
        id: int = Query(..., description="用户ID"),
):
    user = await user_controller.get(id=id)
    await user_controller.update_roles(user, data["ids"])
    return Success(msg="Updated Successfully")


@userRouter.post("/resetPwd", summary="重置用户密码")
async def reset_pwd(
        data: dict,
):
    user = await user_controller.get(id=data["id"])
    user.password = get_password_hash(data["newPwd"])
    await user.save()
    return Success(msg="Reset Successfully")

