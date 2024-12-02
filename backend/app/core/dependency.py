import jwt
from fastapi import Depends, Header, HTTPException, Request

from app.core.ctx import CTX_USER_ID
from app.models import Role, User
from app.schemas.users import UserPydantic
from app.settings import settings
from app.utils.log import logger


class DataBaseControl:
    @classmethod
    async def has_db(cls, request: Request) -> bool:
        # 设置数据库未配置时的白名单
        whit_list = ["/api/v1/admin/test_db_info", "/api/v1/admin/set_db_info"]
        if (settings.DATABASE_START is not None) or request.url.path in whit_list:
            return True
        else:
            logger.error("数据库未配置！")
            raise HTTPException(status_code=403, detail="数据库未配置！禁止访问！")


class AuthControl:
    @classmethod
    async def is_authed(cls, authorization: str = Header(..., description="token验证"),
                        db: bool = Depends(DataBaseControl.has_db)) -> UserPydantic:
        if db:
            try:
                token = authorization.split(" ")[1]
                decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
                user_id = decode_data.get("user_id")
                username = decode_data.get("username")
                if settings.DATABASE_START is None and username == settings.SUPER_USER["username"]:
                    return UserPydantic.parse_obj(settings.SUPER_USER)
                else:
                    user = await User.filter(id=user_id).first()
                if not user:
                    raise HTTPException(status_code=401, detail="Authentication failed")
                CTX_USER_ID.set(int(user_id))
                return user
            except jwt.DecodeError:
                raise HTTPException(status_code=401, detail="无效的Token")
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="登录已过期")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"{repr(e)}")


class PermissionControl:
    @classmethod
    async def has_permission(cls, request: Request, current_user: User = Depends(AuthControl.is_authed)) -> None:
        if current_user.is_superuser:
            return
        method = request.method
        path = request.url.path
        roles: list[Role] = await current_user.roles
        if not roles:
            raise HTTPException(status_code=403, detail="The user is not bound to a role")
        apis = [await role.apis for role in roles]
        logger.debug(f"{current_user.username} 访问了 {method} {path} 接口")
        permission_apis = list(set((api.method, api.path) for api in sum(apis, [])))
        # path = "/api/v1/auth/userinfo"
        # method = "GET"
        if (method, path) not in permission_apis:
            raise HTTPException(status_code=403, detail=f"Permission denied method:{method} path:{path}")


DependAuth = Depends(AuthControl.is_authed)
DependPermission = Depends(PermissionControl.has_permission)
