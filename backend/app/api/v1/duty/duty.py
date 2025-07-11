# coding=utf-8
# @FileName  :duty.py
# @Time      :2024/7/6 下午7:20
# @Author    :dayezi
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.utils.log import logger
from app.controllers.dutyLog import dutyNotesController, dutyLogController
from app.controllers.material import dutyOverListController
from app.schemas import Success, SuccessExtra, Fail
from app.schemas.dutyLog import DutyOverInfo
from app.utils.onDutyInfo import OnDutyInfo

router = APIRouter()


@router.post("/dutyOver", summary="接班")
async def duty_over(
        data: DutyOverInfo,
        area: str = Query("glb", description="区域"),
        metaType: str = Query("", description="物资类型")
):
    note = await dutyNotesController.create(data.materialNote)
    await dutyLogController.create_all(data.materialData, note)
    onDutyInfo = OnDutyInfo()
    onDutyInfo.setDutyInfo(
        area,
        metaType,
        data.dutyPerson,
        data.dutyPersonDepart)

    result = {
        "dutyPerson": data.dutyPerson,
        "dutyPersonDepart": data.dutyPersonDepart
    }
    return Success(data=result)


@router.get("/getDutyNote", summary="获取值班备注")
async def get_duty_note(id: int = Query(..., description="值班备注id")):
    data = await dutyNotesController.get(id)
    data = await data.to_dict()
    return Success(data=data)


@router.get("/latestNote", summary="获取最近一条备注")
async def get_latest_note(
        area: str = Query("glb", description="物资区域"),
        metaType: str = Query("tool", description="物资类型")
):
    q = Q(Q(area__contains=area), Q(type__contains=metaType))
    data = await dutyNotesController.latest(search=q)
    if data:
        data = await data.to_dict()
    else:
        data = ""
    return Success(data=data)


@router.get("/dutyPerson", summary="获取岗位值班人员信息")
async def get_duty_info(
        area: str = Query("glb", description="物资区域"),
        metaType: str = Query("", description="物资类型"),
):
    info = OnDutyInfo()
    data = info.getDutyInfo(area, metaType)
    return Success(data=data)


@router.get("/7s/list", summary="获取接班7S清单")
async def get_duty_over_list(area: str = Query("glb", description="部门")):
    q = Q(area__contains=area)
    total, duty_over_list_objs = await dutyOverListController.list(page=1, page_size=1000, search=q)
    data = [await obj.to_dict() for obj in duty_over_list_objs]
    return SuccessExtra(msg="接班清单获取成功", data=data,
                        total=total, page=1, pageSize=1000)


@router.post("/7s/update", summary="更新接班7S清单")
async def update_duty_over_list(
        data: list[dict], area: str = Query("glb", description="部门")):
    for item in data:
        if item.get("id"):
            await dutyOverListController.update(item["id"], item)
        else:
            item["area"] = area
            await dutyOverListController.create(item)
    return Success(msg="更新成功")


@router.delete("/7s/delete", summary="删除接班7S清单")
async def delete_duty_over_list(id: int):
    try:
        await dutyOverListController.remove(id)
    except Exception as e:
        logger.error(f"删除接班清单项失败，ID为{id}")
        return Fail(msg=f"删除接班清单项部分失败: {e}")
    return Success(msg="删除成功")
