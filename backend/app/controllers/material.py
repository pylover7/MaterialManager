from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from app.core.crud import CRUDBase, CreateSchemaType, ModelType
from app.models.material import Material, AttentionNote
from app.schemas.material import MaterialCreate, MaterialUpdate, AttentionNoteCreate, AttentionNoteUpdate


class MaterialController(CRUDBase[Material, MaterialCreate, MaterialUpdate]):
    def __init__(self):
        super().__init__(Material)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj = await super().create(obj_in)
            return obj
        except IntegrityError:
            raise HTTPException(status_code=403, detail="该物品已存在！")

    async def get_by_name(self, name: str):
        return await self.model.filter(name=name).first()


class MaterialAttentionController(CRUDBase[AttentionNote, AttentionNoteCreate, AttentionNoteUpdate]):
    def __init__(self):
        super().__init__(AttentionNote)


materialController = MaterialController()
materialAttentionController = MaterialAttentionController()
