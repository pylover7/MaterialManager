# coding=utf-8
# @FileName  :__init__.py.py
# @Time      :2024/4/23 上午2:00
# @Author    :dayezi
from fastapi import APIRouter

from .system import sysRouter
from .apis import apiRouter
from .menus import menuRouter
from .roles import roleRouter
from .users import userRouter
from .area import areaRouter

adminRouter = APIRouter()
adminRouter.include_router(sysRouter, tags=["系统数据库模块"], prefix="/system")
adminRouter.include_router(apiRouter, tags=["系统API模块"], prefix="/api")
adminRouter.include_router(menuRouter, tags=["系统菜单模块"], prefix="/menu")
adminRouter.include_router(roleRouter, tags=["系统角色模块"], prefix="/role")
adminRouter.include_router(userRouter, tags=["系统用户模块"], prefix="/user")
adminRouter.include_router(areaRouter, tags=["系统区域模块"], prefix="/area")

__all__ = ["adminRouter"]
