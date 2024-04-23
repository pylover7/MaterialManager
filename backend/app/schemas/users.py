from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import User, Depart

UserPydantic = pydantic_model_creator(User)


class UserCreate(UserPydantic):
    ...

    def create_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"roles"})


class UserUpdate(UserPydantic):
    ...

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"roles", "id"})


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
    ...

    def update_dict(self):
        return self.model_dump(exclude_unset=True)


if __name__ == '__main__':
    print(UserPydantic.schema())
