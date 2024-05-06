from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import User, Depart

UserPydantic = pydantic_model_creator(User)


class UserCreate(UserPydantic):
    is_superuser: bool = False
    last_login: str = None
    departId: int = None
    avatar: str = None
    uuid: str = None

    def create_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"roles", "depart"})


class UserUpdate(UserPydantic):
    id: int
    last_login: str = None
    password: str = None
    departId: int = Field(description="部门ID")

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"roles", "id"})


class UpdateStatus(BaseModel):
    id: int = Field(description="用户ID")
    status: int = Field(description="状态")


class UpdatePassword(BaseModel):
    id: int = Field(description="用户ID")
    old_password: str = Field(description="旧密码")
    new_password: str = Field(description="新密码")


DepartPydantic = pydantic_model_creator(Depart)


class DepartCreate(DepartPydantic):
    ...

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class DepartUpdate(DepartPydantic):
    id: int = Field(description="部门ID")

    def update_dict(self):
        return self.model_dump(exclude_unset=True)


if __name__ == '__main__':
    print(DepartCreate.schema())
