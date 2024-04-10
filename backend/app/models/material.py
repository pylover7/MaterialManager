from tortoise import fields

from .base import Material


class GlbMaterial(Material):
  
  class Meta:
    table = "glb_material"
    
class FkMaterial(Material):
  
  class Meta:
    table = "fk_material"

class WkMaterial(Material):
  
  class Meta:
    table = "wk_material"
  