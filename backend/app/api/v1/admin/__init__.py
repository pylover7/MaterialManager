# coding=utf-8
# @FileName  :__init__.py.py
# @Time      :2024/4/23 上午2:00
# @Author    :dayezi
from fastapi import APIRouter

from .depart import departRouter
from .system import sysRouter
from .apis import apiRouter
from .menus import menuRouter
from .roles import roleRouter
from .users import userRouter

adminRouter = APIRouter()
adminRouter.include_router(departRouter, tags=["系统部门模块"], prefix="/depart")
adminRouter.include_router(sysRouter, tags=["系统数据库模块"], prefix="/system")
adminRouter.include_router(apiRouter, tags=["系统API模块"], prefix="/api")
adminRouter.include_router(menuRouter, tags=["系统菜单模块"], prefix="/menu")
adminRouter.include_router(roleRouter, tags=["系统角色模块"], prefix="/role")
adminRouter.include_router(userRouter, tags=["系统用户模块"], prefix="/user")

__all__ = ["adminRouter"]
