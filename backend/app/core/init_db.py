# coding=utf-8
# @FileName  :init_db.py
# @Time      :2024/4/16 上午2:53
# @Author    :dayezi
from fastapi import FastAPI
from tortoise import Tortoise
import pymysql

from app.controllers import user_controller
from app.schemas.users import UserCreate
from app.settings import settings
from app.log import logger
from app.schemas.admin import DbInfo
from app.core.init_menus import init_api, init_menus, init_roles
from app.utils import generate_uuid


async def init_db(app: FastAPI):
    if settings.DATABASE_START:
        await tortoise_init(app)


async def tortoise_init(app: FastAPI):
    logger.info("正在初始化数据库...")
    await Tortoise.init(config=settings.TORTOISE_ORM)
    logger.info("数据库初始化完成")
    logger.info("正在生成数据库表...")
    await Tortoise.generate_schemas(safe=True)
    logger.info("数据库表生成完成")
    await init_api(app)
    await init_menus()
    await init_roles()
    await register_superAdmin()


async def register_superAdmin():
    user = await user_controller.model.exists()
    if not user:
        logger.info("正在注册超级管理员...")
        settings.SUPER_USER["uuid"] = generate_uuid(settings.SUPER_USER["username"])
        await user_controller.create(UserCreate.parse_obj(settings.SUPER_USER))
        logger.info("超级管理员注册完成")


def test_db(db_info: DbInfo) -> bool:
    try:
        conn = pymysql.connect(
            host=db_info.host,
            user=db_info.username,
            password=db_info.password,
            db=db_info.database,
            port=db_info.port)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] != 1:
                logger.info("数据库测试失败，失败原因：数据库连接失败")
                return False
        logger.info("数据库测试成功")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"数据库测试失败，失败原因：{e}")
        return False


async def set_db(db_info: DbInfo, app: FastAPI):
    settings.DATABASE_START = db_info.start
    settings.DATABASE_HOST = db_info.host
    settings.DATABASE_PORT = db_info.port
    settings.DATABASE_USERNAME = db_info.username
    settings.DATABASE_PASSWORD = db_info.password
    settings.DATABASE_NAME = db_info.database

    await tortoise_init(app)
