# coding=utf-8
# @FileName  :init_menus.py
# @Time      :2024/4/26 下午3:51
# @Author    :dayezi
from fastapi import FastAPI

from app.controllers import role_controller
from app.models import Menu, Api, Role


async def init_roles(apiIdList: list, menuIdList: list):
    """
    初始化角色
    :return:
    """
    roles = await Role.exists()
    if not roles:
        superAdmin = await Role.create(
            name="超级管理员",
            code="super",
            status=1,
            description="超级管理员",
        )
        await role_controller.update_roles(role=superAdmin, menu_ids=menuIdList, api_ids=apiIdList)
        await Role.create(
            name="普通用户",
            code="common",
            status=1,
            description="普通用户",
        )
        return superAdmin


async def init_api(app: FastAPI):
    """
    初始化API
    :param app:
    :return:
    """
    api = await Api.exists()
    apiList = []
    if not api:
        apis = app.openapi()["paths"]
        for path, value in apis.items():
            for method, value2 in value.items():
                tag = ",".join(value2.get("tags"))
                summary = value2.get("summary")
                api_obj = await Api.create(
                    path=path,
                    method=method.upper(),
                    tags=tag,
                    summary=summary
                )
                apiList.append(api_obj.id)
    return apiList


async def init_menus():
    """
    初始化菜单
    :return:
    """
    menus = await Menu.exists()
    menuList = []
    if not menus:
        glb = await Menu.create(
            parentId=0,
            menuType=0,
            title="隔离办",
            name="Glb",
            path="/glb",
            component="",
            rank=1,
            redirect="",
            icon="fluent:desktop-flow-24-regular",
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
        menuList.append(glb.id)
        glb_children = [
            await Menu.create(
                parentId=glb.id,
                menuType=0,
                title="隔离办物资管理",
                name="GlbMaterial",
                path="/glb/material",
                icon="fluent:box-search-16-regular",
            ),
            await Menu.create(
                parentId=glb.id,
                menuType=0,
                title="隔离办钥匙管理",
                name="GlbKey",
                path="/glb/key",
                icon="fluent:key-reset-24-regular",
            ),
        ]
        for item in glb_children:
            menuList.append(item.id)

        fk = await Menu.create(
            parentId=0,
            menuType=0,
            title="辅控",
            name="Fk",
            path="/fk",
            component="",
            rank=2,
            redirect="",
            icon="fluent:brain-circuit-24-regular",
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
        menuList.append(fk.id)
        fk_children = [
            await Menu.create(
                parentId=fk.id,
                menuType=0,
                title="辅控物资管理",
                name="FkMaterial",
                path="/fk/material",
                icon="fluent:box-search-16-regular",
            ),
            await Menu.create(
                parentId=fk.id,
                menuType=0,
                title="辅控钥匙管理",
                name="FkKey",
                path="/fk/key",
                icon="fluent:key-reset-24-regular",
            )
        ]
        for item in fk_children:
            menuList.append(item.id)

        wk = await Menu.create(
            parentId=0,
            menuType=0,
            title="网控",
            name="Wk",
            path="/wk",
            component="",
            rank=3,
            redirect="",
            icon="fluent:desktop-flow-24-regular",
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
        menuList.append(wk.id)
        wk_children = [
            await Menu.create(
                parentId=wk.id,
                menuType=0,
                title="网控物资管理",
                name="WkMaterial",
                path="/wk/material",
                icon="fluent:box-search-16-regular",
            ),
            await Menu.create(
                parentId=wk.id,
                menuType=0,
                title="网控钥匙管理",
                name="WkKey",
                path="/wk/key",
                icon="fluent:key-reset-24-regular",
            ),
        ]
        for item in wk_children:
            menuList.append(item.id)

        admin = await Menu.create(
            parentId=0,
            menuType=0,
            title="管理员",
            name="Admin",
            path="/admin",
            component="",
            rank=5,
            redirect="",
            icon="fluent:shield-person-20-regular",
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
        menuList.append(admin.id)
        admin_children = [
            await Menu.create(
                parentId=admin.id,
                menuType=0,
                title="审批",
                name="Approval",
                path="/admin/approval",
                icon="fluent:person-edit-48-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=admin.id,
                menuType=0,
                title="物资数据",
                name="MaterialMeta",
                path="/admin/material-meta",
                icon="fluent:home-garage-24-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=admin.id,
                menuType=0,
                title="日志审计",
                name="OperationLogs",
                path="/admin/operation-logs",
                icon="fluent:notepad-person-24-regular",
                keepAlive=True,
            ),
        ]
        for item in admin_children:
            menuList.append(item.id)

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
        menuList.append(chaoGuan.id)
        chaoGuan_children = [
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                title="用户管理",
                name="UserManagement",
                path="/superAdmin/userManagement",
                icon="fluent:people-team-20-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                title="部门管理",
                name="DeptManagement",
                path="/superAdmin/deptManagement",
                icon="fluent:people-community-20-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                title="角色管理",
                name="RoleManagement",
                path="/superAdmin/roleManagement",
                icon="fluent:people-team-20-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                title="菜单管理",
                name="MenuManagement",
                path="/superAdmin/menuManagement",
                icon="fluent:clover-48-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                title="系统日志",
                name="Logs",
                path="/superAdmin/logs",
                icon="fluent:text-bullet-list-square-search-20-regular",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                title="系统设置",
                name="Settings",
                path="/superAdmin/settings",
                icon="fluent:settings-48-regular",
                keepAlive=True,
            ),
        ]
        for item in chaoGuan_children:
            menuList.append(item.id)
    return menuList
