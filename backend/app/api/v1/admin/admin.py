# coding=utf-8
# @FileName  :users.py
# @Time      :2024/4/16 下午9:31
# @Author    :dayezi
from fastapi import APIRouter

from app.settings import settings
from app.core.init_db import test_db, set_db
from app.log import logger
from app.schemas import Success, Fail
from app.schemas.admin import DbInfo

router = APIRouter()


@router.get("/get_db_info")
async def get_db_info():
    data = settings.DATABASE_INFO.model_dump()
    return Success(data=data)


@router.post("/test_db_info", summary="测试数据库连接")
async def test_db_conn(data: DbInfo):
    if test_db(data):
        return Success(msg="数据库链接成功！")
    else:
        return Fail(msg="数据库链接失败！")


@router.post("/set_db_info", summary="设置数据库连接")
async def set_db_conn(data: DbInfo):
    try:
        await set_db(data)
        return Success(msg="数据库设置成功！")
    except Exception as e:
        logger.error(e)
        return Fail(msg="数据库设置失败！")
