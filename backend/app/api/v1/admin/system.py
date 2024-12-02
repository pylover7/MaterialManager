# coding=utf-8
# @FileName  :system.py
# @Time      :2024/7/6 上午3:49
# @Author    :dayezi
from pathlib import Path
from fastapi import APIRouter, Request, Query

from app.settings import settings
from app.core.init_db import test_db, set_db
from app.schemas import Success, Fail, SuccessExtra
from app.schemas.admin import DbInfo
from app.utils.log import logger

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


@sysRouter.get("/getLoginLogs", summary="获取登录日志")
async def get_login_logs(
        currentPage: int = Query(1, description="页码"),
        pageSize: int = Query(15, description="每页数量"),
):
    loginLog = Path(__file__).parent.parent.parent.parent.parent.joinpath("logs", "login.log")
    # 读取 loginLog 下的文件，按照逆序读取，根据currentPage 和 pageSize 分页，并计算总数量total
    data = []
    with open(loginLog, "r") as f:
        lines = f.readlines()
        total = len(lines)
        start_index = total - pageSize * (currentPage - 1)
        end_index = start_index - pageSize
        if end_index < 0:
            end_index = 0
        for i in range(start_index, end_index, -1):
            # 分割日志行
            parts = lines[i - 1].strip().split('|')
            # 构建字典
            log_dict = {
                'username': parts[3].strip(),
                'status': 1 if parts[1].strip() == "SUCCESS" else 0,
                'ip': parts[2].strip(),
                'loginTime': parts[0].strip()
            }
            data.append(log_dict)
    return SuccessExtra(data=data, total=total, currentPage=currentPage, pageSize=pageSize)
