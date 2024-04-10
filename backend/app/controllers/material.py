from app.core.crud import CRUDBase
from app.models.material import Material, AttentionNote
from app.schemas.material import MaterialCreate, MaterialUpdate, AttentionNoteCreate, AttentionNoteUpdate


class MaterialController(CRUDBase[Material, MaterialCreate, MaterialUpdate]):
    def __init__(self):
        super().__init__(Material)

    async def get_by_name(self, name: str):
        return await self.model.filter(name=name).first()


class MaterialNoteController(CRUDBase[AttentionNote, AttentionNoteCreate, AttentionNoteUpdate]):
    def __init__(self):
        super().__init__(AttentionNote)


material_controller = MaterialController()
material_note_controller = MaterialNoteController()
