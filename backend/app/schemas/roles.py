from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.users import Role

RolePydantic = pydantic_model_creator(Role)


class RoleFilter(RolePydantic):
    remark: str = None


class RoleCreate(RolePydantic):
    pass


class RoleUpdate(RolePydantic):
    id: int = Field(example=1)

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class RoleUpdateMenusApis(BaseModel):
    id: int
    menus: list[int] = []
    apis: list[int] = []
    areas: list[int] = []
