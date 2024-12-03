# coding=utf-8
# @FileName  :system.py
# @Time      :2024/7/6 上午3:49
# @Author    :dayezi
from datetime import datetime
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


@sysRouter.post("/getLoginLogs", summary="获取登录日志")
async def get_login_logs(
        data: dict,
        currentPage: int = Query(1, description="页码"),
        pageSize: int = Query(15, description="每页数量"),
):
    loginLog = Path(__file__).parent.parent.parent.parent.parent.joinpath("logs", "login.log")
    # 读取 loginLog 下的文件，按照逆序读取，根据currentPage 和 pageSize 分页，并计算总数量total
    logList = []
    with open(loginLog, "r", encoding="utf-8") as f:
        lines = f.readlines()
        # 对读取的日志先经过username和status，以及startTime和endTime 过滤
        if data["username"]:
            lines = [line for line in lines if data["username"] in line]
        if data["status"]:
            newLines = []
            for line in lines:
                if data["status"] == "1" and "SUCCESS" in line:
                    newLines.append(line)
                elif data["status"] == "0" and "ERROR" in line:
                    newLines.append(line)
            lines = newLines
        if len(data["loginTime"]) > 1:
            lines = [line for line in lines if
                     datetime.strptime(data["loginTime"][0], "%Y-%m-%d %H:%M:%S")
                     <= datetime.strptime(line.split("|")[0].strip(), "%Y-%m-%d %H:%M:%S.%f")
                     <= datetime.strptime(data["loginTime"][1], "%Y-%m-%d %H:%M:%S")]

        total = len(lines)
        if total == 0:
            return SuccessExtra(data=logList, total=total, currentPage=currentPage, pageSize=pageSize)
        start_index = total - pageSize * (currentPage - 1)
        end_index = start_index - pageSize
        if end_index < 0:
            end_index = -1
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
            logList.append(log_dict)
    return SuccessExtra(data=logList, total=total, currentPage=currentPage, pageSize=pageSize)


@sysRouter.get("/clearLoginLogs", summary="清除登录日志")
async def clear_login_logs():
    loginLog = Path(__file__).parent.parent.parent.parent.parent.joinpath("logs", "login.log")
    with open(loginLog, "w", encoding="utf-8") as f:
        f.write("")
    return Success(msg="清除成功！")
