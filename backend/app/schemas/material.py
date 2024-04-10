from typing import Optional

from pydantic import BaseModel, Field


class Material(BaseModel):
    id: int
    name: Optional[str] = None
    model: Optional[str] = None
    position: Optional[str] = None
    number: Optional[str] = None
    depart: Optional[str] = None


class MaterialCreate(BaseModel):
    name: str = Field(description="物资名字")
    model: str = Field(description="物资型号")
    position: str = Field(description="物资位置")
    number: str = Field(description="物资数量")
    depart: str = Field(description="物资所属部门")

    def create_dict(self):
        # 创建字典
        return self.model_dump(exclude_unset=True)


class MaterialUpdate(BaseModel):
    id: int
    name: str = Field(description="物资名字")
    model: str = Field(description="物资型号")
    position: str = Field(description="物资位置")
    number: str = Field(description="物资数量")

    def update_dict(self):
        # 更新字典
        return self.model_dump(exclude_unset=True, exclude={"id"})
