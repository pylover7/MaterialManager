from datetime import timedelta
import base64

from fastapi import APIRouter, Request
from jwt.exceptions import ExpiredSignatureError

from app.controllers.user import user_controller
from app.core.ctx import CTX_USER_ID
from app.core.dependency import DependAuth
from app.models import MaterialArea
from app.utils.log import logger
from app.models.users import Api, Menu, Role, User
from app.schemas.base import Success, FailAuth
from app.schemas.login import *
from app.settings import settings
from app.utils import now
from app.utils.jwtt import create_access_token, decode_access_token

router = APIRouter()


@router.post("/accessToken", summary="获取token")
async def login_access_token(request: Request, credentials: CredentialsSchema):
    credentials.password = base64.b64decode(credentials.password).decode("utf-8")
    user = await user_controller.authenticate(credentials, request.client.host)
    await user_controller.update_last_login(user.id)
    roles = await user.roles.all().values_list("code", flat=True)
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = now(0) + access_token_expires
    expire_refresh = now(0) + refresh_token_expires

    data = JWTOut(
        nickname=user.nickname,
        username=user.username,
        uuid=user.uuid.__str__(),
        depart=user.department,
        roles=roles,
        accessToken=create_access_token(
            data=JWTPayload(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser,
                exp=expire,
            )
        ),
        refreshToken=create_access_token(
            data=JWTPayload(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser,
                exp=expire_refresh,
            )
        ),
        expires=expire.strftime("%Y-%m-%d %H:%M:%S")  # expire.timestamp()
    )
    return Success(data=data.model_dump())


@router.post("/refreshToken", summary="刷新token")
async def refresh_token(refreshToken: refreshTokenSchema):
    try:
        payload = decode_access_token(refreshToken.refreshToken)
        logger.info(f"refreshToken有效截至时间：{payload.exp.strftime('%Y-%m-%d %H:%M:%S')}（{payload.exp.timestamp()}）， "
                    f"当前时间：{now()}（{now(2)}）[f{payload.exp.timestamp() - now(2)}]")
        if payload.exp.timestamp() < now(2):
            raise ExpiredSignatureError
    except ExpiredSignatureError:
        return FailAuth(msg="refreshToken已过期")
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + access_token_expires
    expire_refresh = datetime.now() + refresh_token_expires

    data = JWTReOut(
        accessToken=create_access_token(
            data=JWTPayload(
                user_id=payload.user_id,
                username=payload.username,
                is_superuser=payload.is_superuser,
                exp=expire,
            )
        ),
        refreshToken=create_access_token(
            data=JWTPayload(
                user_id=payload.user_id,
                username=payload.username,
                is_superuser=payload.is_superuser,
                exp=expire_refresh,
            )
        ),
        expires=expire.strftime("%Y-%m-%d %H:%M:%S")  # expire.timestamp()
    )

    return Success(data=data.model_dump())


@router.post("/auth", summary="用户验证")
async def auth(request: Request, credentials: CredentialsSchema):
    credentials.password = base64.b64decode(credentials.password).decode("utf-8")
    user = await user_controller.authenticate(credentials, request.client.host)
    data = {
        "uuid": user.uuid.__str__(),
        "username": user.username,
        "nickname": user.nickname,
        "phone": user.mobile,
        "depart": user.department
    }
    return Success(data=data)


@router.get("/userInfos", summary="查看本人信息", dependencies=[DependAuth])
async def get_userinfo():
    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    data = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=data)


@router.get("/userMenu", summary="获取本人菜单", dependencies=[DependAuth])
async def get_user_menu():
    user_id = CTX_USER_ID.get()
    user_obj = await User.filter(id=user_id).first()
    menus: list[Menu] = []
    if user_obj.is_superuser:
        menus = await Menu.all()
    else:
        role_objs: list[Role] = await user_obj.roles
        for role_obj in role_objs:
            menu = await role_obj.menus
            menus.extend(menu)
        menus = list(set(menus))
    parent_menus: list[Menu] = []
    for menu in menus:
        if menu.parentId == 0:
            parent_menus.append(menu)
    res = []
    for parent_menu in parent_menus:
        parent_menu_dict = await parent_menu.to_dict()
        parent_menu_dict["children"] = []
        parent_menu_dict["meta"] = {}
        parent_menu_dict["meta"]["title"] = parent_menu_dict["title"]
        parent_menu_dict["meta"]["icon"] = parent_menu_dict["icon"]
        parent_menu_dict["meta"]["showLink"] = parent_menu_dict["showLink"]
        parent_menu_dict["meta"]["rank"] = parent_menu_dict["rank"]

        async def menuTree(parent_menu_dict: dict) -> dict:
            for menu in menus:
                if menu.parentId == parent_menu_dict["id"]:
                    # roles = await menu.roles.all().values_list("code", flat=True)
                    children_menu = await menu.to_dict()
                    children_menu["children"] = []
                    children_menu["meta"] = {}
                    children_menu["meta"]["title"] = children_menu["title"]
                    children_menu["meta"]["icon"] = children_menu["icon"]
                    children_menu["meta"]["extraIcon"] = children_menu["extraIcon"]
                    children_menu["meta"]["showLink"] = children_menu["showLink"]
                    children_menu["meta"]["showParent"] = children_menu["showParent"]
                    # children_menu["meta"]["roles"] = roles
                    children_menu["meta"]["auths"] = children_menu["auths"]
                    children_menu["meta"]["keepAlive"] = children_menu["keepAlive"]
                    children_menu["meta"]["frameSrc"] = children_menu["frameSrc"]
                    children_menu["meta"]["frameLoading"] = children_menu["frameLoading"]
                    children_menu["meta"]["frameLoading"] = children_menu["frameLoading"]
                    children_menu["meta"]["hiddenTag"] = children_menu["hiddenTag"]
                    children_menu["meta"]["dynamicLevel"] = children_menu["dynamicLevel"]
                    children_menu["meta"]["activePath"] = children_menu["activePath"]
                    children_menu["meta"]["transition"] = {}
                    children_menu["meta"]["transition"]["name"] = children_menu["transitionName"]
                    children_menu["meta"]["transition"]["enterTransition"] = children_menu["enterTransition"]
                    children_menu["meta"]["transition"]["leaveTransition"] = children_menu["leaveTransition"]

                    parent_menu_dict["children"].append(children_menu)

            parent_menu_dict["children"].sort(key=lambda x: x["rank"])
            if len(parent_menu_dict["children"]) == 0:
                del parent_menu_dict["children"]
                return parent_menu_dict
            for i, v in enumerate(parent_menu_dict["children"]):
                parent_menu_dict["children"][i] = await menuTree(v)
            return parent_menu_dict

        parent_menu_dict = await menuTree(parent_menu_dict)
        res.append(parent_menu_dict)
    return Success(data=res)


@router.get("/userApi", summary="查看本人API", dependencies=[DependAuth])
async def get_user_api():
    user_id = CTX_USER_ID.get()
    user_obj = await User.filter(id=user_id).first()
    if user_obj.is_superuser:
        api_objs: list[Api] = await Api.all()
        apis = [api.method.lower() + api.path for api in api_objs]
        return Success(data=apis)
    role_objs: list[Role] = await user_obj.roles
    apis = []
    for role_obj in role_objs:
        api_objs: list[Api] = await role_obj.apis
        apis.extend([api.method.lower() + api.path for api in api_objs])
    apis = list(set(apis))
    return Success(data=apis)


@router.get("/userArea", summary="查看本人授权区域", dependencies=[DependAuth])
async def get_user_area():
    user_id = CTX_USER_ID.get()
    user_obj = await User.filter(id=user_id).first()
    if user_obj.is_superuser:
        area_objs: list[MaterialArea] = await MaterialArea.all()
        areas = [await area.to_dict() for area in area_objs]
        return Success(data=areas)
    role_objs: list[Role] = await user_obj.roles
    areas = []
    for role_obj in role_objs:
        area_obj: list[MaterialArea] = await role_obj.areas
        for area in area_obj:
            if not area.status:
                break
            areas.append(await area.to_dict())
    seen = set()
    areas = [area for area in areas if area["code"] not in seen and not seen.add(area["code"])]
    return Success(data=areas)
