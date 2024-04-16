from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException, Request

from app.core.ctx import CTX_USER_ID
from app.models import Role, User
from app.settings import settings


class DataBaseControl:
    @classmethod
    async def has_db(cls) -> bool:
        if settings.DATABASE_START is not None:
            return True
        else:
            raise HTTPException(status_code=402, detail="数据库未配置！")


class AuthControl:
    @classmethod
    async def is_authed(cls, authorization: str = Header(..., description="token验证"),
                        db: bool = Depends(DataBaseControl.has_db)) -> Optional["User"]:
        if db:
            try:
                token = authorization.split(" ")[1]
                decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
                user_id = decode_data.get("user_id")
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
        permission_apis = list(set((api.method, api.path) for api in sum(apis, [])))
        # path = "/api/v1/auth/userinfo"
        # method = "GET"
        if (method, path) not in permission_apis:
            raise HTTPException(status_code=403, detail=f"Permission denied method:{method} path:{path}")


DependAuth = Depends(AuthControl.is_authed)
DependPermission = Depends(PermissionControl.has_permission)
