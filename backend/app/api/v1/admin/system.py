# coding=utf-8
# @FileName  :system.py
# @Time      :2024/7/6 上午3:49
# @Author    :dayezi
from fastapi import APIRouter, Request

from app.settings import settings
from app.core.init_db import test_db, set_db
from app.schemas import Success, Fail
from app.schemas.admin import DbInfo
from app.log import logger

sysRouter = APIRouter()


@sysRouter.get("/db/get", summary="获取数据库信息")
async def get_db_info():
    data = settings.DATABASE_INFO.model_dump()
    return Success(data=data)


@sysRouter.post("/db/test", summary="测试数据库连接")
async def test_db_conn(data: DbInfo):
    if test_db(data):
        return Success(msg="数据库链接成功！")
    else:
        return Fail(msg="数据库链接失败！")


@sysRouter.post("/db/set", summary="设置数据库连接")
async def set_db_conn(data: DbInfo, request: Request):
    try:
        await set_db(data, request.app)
        return Success(msg="数据库设置成功！")
    except Exception as e:
        logger.error(e)
        return Fail(msg="数据库设置失败！")
