from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID


class Material(BaseModel):
    id: int
    name: Optional[str] = None
    model: Optional[str] = None
    position: Optional[str] = None
    number: Optional[int] = None
    depart: Optional[str] = None


class MaterialCreate(BaseModel):
    name: str = Field(description="物资名字")
    model: str = Field(description="物资型号")
    position: str = Field(description="物资位置")
    number: int = Field(description="物资数量")
    depart: str = Field(description="物资所属部门")
    uuid: UUID = None

    def create_dict(self):
        # 创建字典
        return self.model_dump(exclude_unset=True)


class MaterialUpdate(BaseModel):
    id: int
    name: str = Field(description="物资名字")
    model: str = Field(description="物资型号")
    position: str = Field(description="物资位置")
    number: int = Field(description="物资数量")

    def update_dict(self):
        # 更新字典
        return self.model_dump(exclude_unset=True, exclude={"id", "uuid"})


class AttentionNote(BaseModel):
    id: int
    note: Optional[str] = None
    depart: Optional[str] = None


class AttentionNoteCreate(BaseModel):
    note: str = Field(description="注意事项")
    depart: str = Field(description="所属部门")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class AttentionNoteUpdate(BaseModel):
    note: str = Field(description="注意事项")
    depart: str = Field(description="所属部门")

    def update_dict(self):
        return self.model_dump(exclude_unset=True)
