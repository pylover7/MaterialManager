from app.core.crud import CRUDBase
from app.models.material import GlbMaterial
from app.schemas.material import MaterialCreate, MaterialUpdate

class GlbMaterialController(CRUDBase[GlbMaterial, MaterialCreate, MaterialUpdate]):
  def __init__(self):
    super().__init__(GlbMaterial)
  
  async def get_by_name(self, name: str):
    return await self.model.filter(name=name).first()