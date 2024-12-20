# coding=utf-8
# @FileName  :init_menus.py
# @Time      :2024/4/26 下午3:51
# @Author    :dayezi
from fastapi import FastAPI

from app.utils.log import logger
from app.models import Menu, Api, Role


async def init_roles():
    """
    初始化角色
    :return:
    """
    roles = await Role.exists()
    if not roles:
        logger.info("正在初始化角色...")
        await Role.create(
            name="普通用户",
            code="common",
            status=1,
            description="普通用户",
        )
        logger.info("角色初始化完成")


async def init_api(app: FastAPI):
    """
    初始化API
    :param app:
    :return:
    """
    logger.info("正在注册API...")
    apiOld = await Api.all()
    apiList = []
    apis = app.openapi()["paths"]
    for path, value in apis.items():
        for method, value2 in value.items():
            tag = ",".join(value2.get("tags"))
            summary = value2.get("summary")
            if len(apiOld) == 0:
                api = Api(
                    path=path,
                    method=method.upper(),
                    tags=tag,
                    summary=summary
                )
                apiList.append(api)
            else:
                apiIsNew = True
                for api in apiOld:
                    if api.path == path:
                        apiIsNew = False
                        api.method = method.upper()
                        api.summary = summary
                        api.tags = tag
                        await api.save()
                        break
                if apiIsNew:
                    api = Api(
                        path=path,
                        method=method.upper(),
                        tags=tag,
                        summary=summary
                    )
                    apiList.append(api)
    await Api.bulk_create(apiList)
    logger.info("API初始化完成...")


async def init_menus():
    """
    初始化菜单
    :return:
    """
    menus = await Menu.exists()
    menuList = []
    if not menus:
        logger.info("正在初始化菜单...")
        glb = await Menu.create(
            parentId=0,
            menuType=0,
            title="隔离办",
            name="Glb",
            path="/glb",
            component="",
            rank=1,
            redirect="",
            icon="Glb",
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
                component="material/glbTool",
                icon="Material",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=glb.id,
                menuType=0,
                title="隔离办钥匙管理",
                name="GlbKey",
                path="/glb/key",
                component="material/glbKey",
                icon="Key",
                keepAlive=True,
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
            icon="Fk",
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
                component="material/fkTool",
                icon="Material",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=fk.id,
                menuType=0,
                title="辅控钥匙管理",
                name="FkKey",
                path="/fk/key",
                component="material/fkKey",
                icon="Key",
                keepAlive=True,
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
            icon="Wk",
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
                component="material/wkTool",
                icon="Material",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=wk.id,
                menuType=0,
                title="网控钥匙管理",
                name="WkKey",
                path="/wk/key",
                component="material/wkKey",
                icon="Key",
                keepAlive=True,
            ),
        ]
        for item in wk_children:
            menuList.append(item.id)

        duty = await Menu.create(
            parentId=0,
            menuType=0,
            title="值班员",
            name="Duty",
            path="/duty",
            icon="dutyPerson",
            rank=4,
        )
        menuList.append(duty.id)
        duty_children = [
            await Menu.create(
                parentId=duty.id,
                menuType=0,
                rank=0,
                title="审批",
                name="Approval",
                path="/duty/approval",
                component="admin/Approval",
                icon="Approval",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=duty.id,
                menuType=0,
                rank=1,
                title="物资数据",
                name="MaterialMeta",
                path="/duty/material-meta",
                component="admin/MaterialMeta",
                icon="MaterialMeta",
                keepAlive=True,
            ),
        ]
        for item in duty_children:
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
            icon="Admin",
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
                rank=2,
                title="物资送检",
                name="MaterialChecked",
                path="/admin/MaterialChecked",
                component="admin/MaterialChecked",
                icon="MaterialChecked",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=admin.id,
                menuType=0,
                rank=3,
                title="日志审计",
                name="OperationLogs",
                path="/admin/operation-logs",
                component="admin/OperationLogs",
                icon="OperationLogs",
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
            icon="superAdmin",
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
                component="superAdmin/UserManagement/index",
                icon="UserManagement",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                rank=2,
                title="角色管理",
                name="RoleManagement",
                path="/superAdmin/RoleManagement",
                component="superAdmin/roleManagement/index",
                icon="RoleManagement",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                rank=3,
                title="菜单管理",
                name="MenuManagement",
                path="/superAdmin/MenuManagement",
                component="superAdmin/menuManagement/index",
                icon="MenuManagement",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                rank=4,
                title="区域管理",
                name="AreaManagement",
                path="/superAdmin/AreaManagement",
                component="superAdmin/areaManagement/index",
                icon="AreaManagement",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                rank=5,
                title="系统日志",
                name="Logs",
                path="/superAdmin/logs",
                component="superAdmin/Logs",
                icon="Logs",
                keepAlive=True,
            ),
            await Menu.create(
                parentId=chaoGuan.id,
                menuType=0,
                rank=6,
                title="系统设置",
                name="Settings",
                path="/superAdmin/settings",
                component="superAdmin/Settings",
                icon="Settings",
                keepAlive=True,
            ),
        ]
        for item in chaoGuan_children:
            menuList.append(item.id)
        logger.info("菜单初始化完成")
    return menuList
