from app.core.crud import CRUDBase
from app.models import MaterialArea
from app.models.users import Api, Menu, Role
from app.schemas.roles import RoleCreate, RoleUpdate


class RoleController(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self):
        super().__init__(model=Role)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

    async def update_roles(
            self, role: Role, menu_ids: list[int], api_ids: list[int], area_ids: list[int]) -> None:
        await role.menus.clear()
        for menu_id in menu_ids:
            menu_obj = await Menu.filter(id=menu_id).first()
            await role.menus.add(menu_obj)

        await role.apis.clear()
        for api_id in api_ids:
            api_obj = await Api.filter(id=api_id).first()
            await role.apis.add(api_obj)

        await role.areas.clear()
        for area_id in area_ids:
            area_obj = await MaterialArea.filter(id=area_id).first()
            await role.areas.add(area_obj)

    async def setDefault(self, id: int):
        await self.model.filter().update(default=0)
        await self.model.filter(id=id).update(default=1)


role_controller = RoleController()
