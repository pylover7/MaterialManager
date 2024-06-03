from datetime import timedelta

from fastapi import APIRouter
from jwt.exceptions import ExpiredSignatureError

from app.controllers.depart import departController
from app.controllers.user import user_controller
from app.core.ctx import CTX_USER_ID
from app.core.dependency import DependAuth
from app.models.users import Api, Menu, Role, User
from app.schemas.base import Fail, Success, FailAuth
from app.schemas.login import *
from app.schemas.users import UpdatePassword, UserPydantic
from app.settings import settings
from app.utils.jwtt import create_access_token, decode_access_token
from app.utils.password import get_password_hash, verify_password

router = APIRouter()


@router.post("/accessToken", summary="获取token")
async def login_access_token(credentials: CredentialsSchema):
    if (settings.DATABASE_START is None and credentials.username == settings.SUPER_USER["username"]
            and credentials.password == settings.SUPER_USER_PWD):
        user = UserPydantic.parse_obj(settings.SUPER_USER)
        roles = user.roles
        depart = user.depart
    else:
        user: User = await user_controller.authenticate(credentials)
        await user_controller.update_last_login(user.id)
        roles = await user.roles.all().values_list("code", flat=True)
        depart = await departController.get_all_name(user)
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + access_token_expires
    expire_refresh = datetime.now() + refresh_token_expires

    data = JWTOut(
        username=user.username,
        uuid=user.uuid.__str__(),
        depart=depart,
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
        if payload.exp < datetime.now():
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


@router.get("/userinfo", summary="查看用户信息", dependencies=[DependAuth])
async def get_userinfo():
    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    data = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=data)


@router.get("/userMenu", summary="查看用户菜单", dependencies=[DependAuth])
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

        for menu in menus:
            if menu.parentId == parent_menu.id:
                # roles = await menu.roles.all().values_list("code", flat=True)
                children_menu = await menu.to_dict()
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
        res.append(parent_menu_dict)
    return Success(data=res)


@router.get("/userapi", summary="查看用户API", dependencies=[DependAuth])
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


@router.post("/updatePwd", summary="更新用户密码", dependencies=[DependAuth])
async def update_user_password(req_in: UpdatePassword):
    user = await user_controller.get(req_in.id)
    verified = verify_password(req_in.old_password, user.password)
    if not verified:
        return Fail(msg="旧密码验证错误！")
    user.password = get_password_hash(req_in.new_password)
    await user.save()
    return Success(msg="修改成功")
