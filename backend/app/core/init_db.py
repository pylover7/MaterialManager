# coding=utf-8
# @FileName  :init_db.py
# @Time      :2024/4/16 上午2:53
# @Author    :dayezi
from tortoise import Tortoise, run_async
import pymysql
from app.settings import settings
from app.log import logger
from app.schemas.admin import DbInfo


async def tortoise_init():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)


def test_db(db_info: DbInfo) -> bool:
    try:
        conn = pymysql.connect(
            host=db_info.db_host,
            user=db_info.db_user,
            password=db_info.db_password,
            db=db_info.db_name,
            port=db_info.db_port)
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
        logger.info(f"数据库测试失败，失败原因：{e}")
        return False


def set_db(db_info: DbInfo):
    settings.DATABASE_START = db_info.db_start
    settings.DATABASE_HOST = db_info.db_host
    settings.DATABASE_PORT = db_info.db_port
    settings.DATABASE_USERNAME = db_info.db_user
    settings.DATABASE_PASSWORD = db_info.db_password
    settings.DATABASE_NAME = db_info.db_name

    run_async(tortoise_init())
