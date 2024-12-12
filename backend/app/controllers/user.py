from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from app.core.crud import CRUDBase
from app.schemas.login import CredentialsSchema
from app.schemas.users import UserCreate, UserUpdate

from .role import role_controller
from ..models import User
from ..utils import now, generate_uuid
from ..utils.cnnp import ldap_auth
from ..utils.log import loginLogger


class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.model.filter(email=email).first()

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.filter(username=username).first()

    async def create(self, obj_in: UserCreate) -> User:
        obj_in.uuid = generate_uuid(obj_in.username)
        try:
            obj = await super().create(obj_in.create_dict())
        except IntegrityError:
            raise HTTPException(status_code=400, detail=f"用户已存在！")
        return obj

    async def update_last_login(self, id: int) -> None:
        user = await self.model.get(id=id)
        user.last_login = datetime.now()
        await user.save()

    async def authenticate(self, credentials: CredentialsSchema, ip: str) -> User:
        # user = await self.model.filter(username=credentials.username).first()
        # ldapUser 有信息就是登录成功
        ldapUser = ldap_auth.get_user_info(credentials.username)
        # 获取数据库中的用户信息，没有就注册一个
        user = await self.get_by_username(credentials.username)
        if not user:
            userCreate = UserCreate(
                username=ldapUser.sAMAccountName,
                nickname=ldapUser.name,
                email=ldapUser.mail,
                mobile=ldapUser.mobile,
                employeeID=ldapUser.employeeID,
                department=ldapUser.department,
                company=ldapUser.company
            )
            user = await self.create(userCreate)
        if now(0) - user.updated_at  < timedelta(hours=1) and user.status == 0:
            remaining_time = 60 - int((now(0) - user.updated_at).total_seconds()) // 60
            raise HTTPException(status_code=400,
                                detail=f"密码错误次数过多，账号已被锁定，请【{remaining_time}】分钟后再尝试登录")
        ldapUser, result = ldap_auth.authenticate(credentials.username, credentials.password)
        if result:
            # 解封
            user.status = 1
            user.loginFail = 0
            await user.save()
            loginLogger.success(credentials.username, ip=ip)
            return user
        else:
            user.loginFail += 1
            if user.loginFail >= 5 and user.status == 1:
                # 锁定
                user.status = 0
            await user.save()
            loginLogger.error(credentials.username, ip=ip)
            raise HTTPException(status_code=400, detail=f"密码错误，尝试登录次数{user.loginFail}/5!")

    async def update_roles(self, user: User, roles: List[int]) -> None:
        await user.roles.clear()
        for role_id in roles:
            role_obj = await role_controller.get(id=role_id)
            await user.roles.add(role_obj)

    async def update_status(self, user: User, status: int) -> None:
        user.status = status
        await user.save()

    async def update_avatar(self, user: User, avatar: str) -> None:
        user.avatar = avatar
        await user.save()


user_controller = UserController()
