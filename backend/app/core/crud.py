from typing import Any, Dict, Generic, List, NewType, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from tortoise.expressions import Q
from tortoise.models import Model

Total = NewType("Total", int)
ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, id: int) -> ModelType | None:
        return await self.model.get_or_none(id=id)

    async def get_by_uuid(self, uuid: str) -> ModelType | None:
        return await self.model.get_or_none(uuid=uuid)

    async def latest(self, search: Q = Q()) -> ModelType:
        return await self.model.filter(search).all().order_by("-id").first()

    async def all(self, search: Q = Q()):
        return await self.model.filter(search).all()

    async def list(self, page: int, page_size: int, search: Q = Q(), order: list = []) -> Tuple[Total, List[ModelType]]:
        query = self.model.filter(search)
        return await query.count(), await query.offset((page - 1) * page_size).limit(page_size).order_by(*order)

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        if isinstance(obj_in, Dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump()
        obj = self.model(**obj_dict)
        await obj.save()
        return obj

    async def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, Dict):
            obj_dict = obj_in
        else:
            obj_dict = obj_in.model_dump(exclude_unset=True)
        obj = await self.get(id=id)
        obj = obj.update_from_dict(obj_dict)
        await obj.save()
        return obj

    async def remove(self, id: int) -> None:
        obj = await self.get(id=id)
        await obj.delete()

    async def children_ids(self, parentId: int) -> List[int]:
        childrenList = [parentId]
        childrenId = await self.model.filter(parentId=parentId).all().values_list("id", flat=True)
        if childrenId:
            childrenList.extend(childrenId)
            for item in childrenId:
                items = await self.children_ids(item)
                if items:
                    childrenList.extend(items)

        return list(set(childrenList))
