from uuid import UUID

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import User

UserPydantic = pydantic_model_creator(User)


class UserCreate(UserPydantic):
    uuid: UUID = None
    is_superuser: bool = False
    last_login: str = None
    avatar: str = None
    remark: str = None

    def create_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"roles", "depart"})


class UserUpdate(UserPydantic):
    id: int
    last_login: str = None
    password: str = None
    departId: int | None = Field(description="部门ID")
    uuid: str = None
    avatar: str = None

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"roles", "id"})


class UpdateStatus(BaseModel):
    id: int = Field(description="用户ID")
    status: int = Field(description="状态")


class UserLdap(BaseModel):
    sAMAccountName: str = Field(description="邮箱前缀")
    employeeID: str = Field(description="工号")
    department: str = Field(description="部门")
    company: str = Field(description="公司")
    mobile: str = Field(description="手机号")
    mail: str = Field(description="邮箱")
    name: str = Field(description="姓名")
    dn: str = Field(description="DN")


class UserLdapCreate(BaseModel):
    username: str
    nickname: str
    email: str
    mobile: str
    employeeID: str
    department: str
    company: str


if __name__ == '__main__':
    pass
