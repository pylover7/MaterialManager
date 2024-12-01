from datetime import datetime
from typing import List, Optional, Tuple

from fastapi.exceptions import HTTPException

from app.core.crud import CRUDBase
from app.schemas.login import CredentialsSchema
from app.schemas.users import UserCreate, UserUpdate
from app.utils.password import get_password_hash, verify_password, md5_encrypt

from .role import role_controller
from ..models import User
from ..utils.cnnp import ldap_auth


class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.model.filter(email=email).first()

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.filter(username=username).first()

    async def create(self, obj_in: UserCreate) -> User:
        obj = await super().create(obj_in.create_dict())
        return obj

    async def update_last_login(self, id: int) -> None:
        user = await self.model.get(id=id)
        user.last_login = datetime.now()
        await user.save()

    async def authenticate(self, credentials: CredentialsSchema) -> User:
        # user = await self.model.filter(username=credentials.username).first()
        ldapUser = ldap_auth.authenticate(credentials.username, credentials.password)
        user = await self.get_by_username(ldapUser.sAMAccountName)
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
        return user

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
