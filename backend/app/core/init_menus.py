# coding=utf-8
# @FileName  :init_menus.py
# @Time      :2024/4/26 下午3:51
# @Author    :dayezi
from app.models import Menu


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
