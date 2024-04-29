from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models.users import Role

RolePydantic = pydantic_model_creator(Role)


class RoleFilter(RolePydantic):
    remark: str = None


class RoleCreate(BaseModel):
    name: str = Field(example="管理员")
    desc: str = Field("", example="管理员角色")


class RoleUpdate(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="管理员")
    desc: str = Field("", example="管理员角色")

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class RoleUpdateMenusApis(BaseModel):
    id: int
    menu_ids: list[int] = []
    api_infos: list[dict] = []
