# coding=utf-8
# @FileName  :init_menus.py
# @Time      :2024/4/26 下午3:51
# @Author    :dayezi
from fastapi import FastAPI

from app.models import Menu, Api
from app.log import logger


async def init_menus():
    menus = await Menu.exists()
    if not menus:
        chaoGuan = await Menu.create(
            parentId=0,
            menuType=0,
            title="超管",
            name="superAdmin",
            path="/superAdmin",
            component="",
            rank=7,
            redirect="",
            icon="fluent:person-passkey-48-regular",
            extraIcon="",
            enterTransition="",
            leaveTransition="",
            activePath="",
            auths="",
            frameSrc="",
            frameLoading=True,
            keepAlive=False,
            hiddenTag=False,
            fixedTag=False,
            showLink=True,
            showParent=False
        )


async def init_api(app: FastAPI):
    api = await Api.exists()
    if not api:
        logger.info("正在注册API...")
        apis = app.openapi()["paths"]
        for path, value in apis.items():
            for method, value2 in value.items():
                tag = ",".join(value2.get("tags"))
                summary = value2.get("summary")
                await Api.create(
                    path=path,
                    method=method.upper(),
                    tags=tag,
                    summary=summary
                )
        logger.info("API注册完成")
