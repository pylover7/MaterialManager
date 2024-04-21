import logging

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.material import materialController, materialAttentionController
from app.controllers.dutyLog import dutyLogController, dutyNotesController
from app.models import Material
from app.schemas.base import Success, SuccessExtra, Fail
from app.schemas.dutyLog import DutyOverInfo
from app.utils.onDutyInfo import OnDutyInfo
from app.schemas.material import MaterialCreate, MaterialUpdate
from app.utils.password import generate_uuid

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/dutyOver", summary="接班")
async def duty_over(data: DutyOverInfo):
    await dutyLogController.create_all(data.materialData)
    await dutyNotesController.create(data.materialNote)
    onDutyInfo = OnDutyInfo()
    await onDutyInfo.setGlbDutyInfo(data.dutyPerson, data.dutyPersonDepart, data.dutyDate)

    result = {
        "dutyPerson": data.dutyPerson,
        "dutyPersonDepart": data.dutyPersonDepart
    }
    return Success(data=result)


@router.get("/meta", summary="获取物资源数据")
async def get_meta(
        depart: str = Query("glb", description="物资部门"),
        page: int = Query(1, description="页码"),
        page_size: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称"),
):
    q = Q(depart__contains=depart)
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await materialController.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="物资数据获取成功", data=data, total=total, page=page, page_size=page_size)


@router.post("/add_meta", summary="添加或修改物资源数据")
async def add_meta(data: MaterialCreate | MaterialUpdate):
    if hasattr(data, "id"):
        result: Material = await materialController.update(data.id, data.update_dict())
    else:
        data: dict = data.model_dump()
        data["uuid"] = generate_uuid(data["name"])
        result: Material = await materialController.create(data)
    result = await result.to_dict()
    if result:
        return Success(data=result)
    else:
        return Fail(msg="数据写入失败！")


@router.delete("/delete", summary="删除物资源数据")
async def delete_meta(data: dict[str, list[int]]):
    for id in data["idList"]:
        try:
            await materialController.remove(id)
        except Exception as e:
            logger.error(f"删除物资项失败，ID为{id}")
            return Fail(msg=f"删除物资项部分失败: {e}")
    return Success(msg="删除成功")


@router.get("/glb_duty_info", summary="获取隔离办值班信息")
async def get_glb_duty_info():
    info = OnDutyInfo()
    data = await info.getGlbDutyInfo()
    return Success(data=data)


@router.get("/glb_attention", summary="获取隔离办物资注意事项")
async def get_glb_attention():
    q = Q(depart__contains="glb")
    total, note_objs = await materialAttentionController.list(page=1, page_size=100, search=q)
    data = [await obj.to_dict() for obj in note_objs]
    return Success(msg="隔离办注意事项", data=data)


@router.get("/glb_latest_note", summary="获取隔离办最近一条备注")
async def get_glb_latest_note():
    q = Q(depart__contains="glb")
    data = await dutyNotesController.latest(search=q)
    if data:
        data = await data.to_dict()
    else:
        data = ""
    return Success(data=data)


@router.get("/fk_material", summary="查看辅控物资列表")
async def get_fk_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称")
):
    q = Q(depart__contains="fk")
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await materialController.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="辅控数据获取成功", data=data, total=total, page=page, page_size=page_size)


@router.get("/wk_material", summary="查看网控物资列表")
async def get_fk_list(
        page: int = Query(1, description="页码"),
        page_size: int = Query(1000, description="每页数量"),
        name: str = Query("", description="物资名称")
):
    q = Q(depart__contains="wk")
    if name:
        q &= Q(name__contains=name)

    total, material_objs = await materialController.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in material_objs]
    return SuccessExtra(msg="网控数据获取成功", data=data, total=total, page=page, page_size=page_size)
