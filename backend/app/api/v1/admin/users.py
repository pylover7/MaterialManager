from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.user import user_controller
from app.models import Role
from app.schemas.base import Success, SuccessExtra
from app.schemas.users import *
from app.utils.cnnp import ldap_auth
from app.utils.log import logger
from app.utils.password import get_password_hash

userRouter = APIRouter()


@userRouter.post("/add", summary="新增用户")
async def create_user(
        data: list[UserCreate],
        role: int | None = Query(None, description="角色ID"),
):
    if role is None:
        role_obj = await Role.filter(default=1).first()
    else:
        role_obj = await Role.get(id=role)
    for item in data:
        try:
            user_obj = await user_controller.create(obj_in=item)
            await user_obj.roles.add(role_obj)
        except Exception as e:
            logger.error(f"用户 {item.nickname} 已存在")
            continue
    return Success(msg="创建成功！")


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
        pageSize: int = Query(15, description="每页数量"),
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

@userRouter.get("/listLdapUser", summary="查看LDAP用户列表")
async def list_ldap_user(
        filterKey: str = Query("sAMAccountName", description="搜索条件字段"),
        filterValue: str = Query("", description="搜索条件值"),
):
    result = ldap_auth.getUserList(filterKey, filterValue)
    return Success(msg="获取成功", data=result)


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

