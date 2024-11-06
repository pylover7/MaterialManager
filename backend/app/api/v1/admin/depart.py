# coding=utf-8
# @FileName  :depart.py
# @Time      :2024/4/23 上午2:00
# @Author    :dayezi
from fastapi import APIRouter

from app.controllers import user_controller
from app.controllers.depart import departController
from app.log import logger
from app.schemas import Success
from app.schemas.users import DepartCreate, DepartUpdate

departRouter = APIRouter()


@departRouter.post("/add", summary="添加部门")
async def add_depart(data: DepartCreate):
    result = await departController.create(data)
    data = await result.to_dict()
    logger.success(f"部门添加成功！{data}")
    return Success(msg="部门添加成功！", data=data)


@departRouter.delete("/delete", summary="删除部门")
async def delete_depart(id: int, name: str):
    await departController.remove(id)
    logger.success(f"【{name}】部门删除成功！")
    return Success(msg="部门删除成功！")


@departRouter.get("/list", summary="获取部门列表")
async def depart_list():
    depart_obj = await departController.all()
    data = []
    for item in depart_obj:
        staffCount = await user_controller.model.filter(depart_id=item.id).count()
        item = await item.to_dict()
        item["staffCount"] = staffCount
        data.append(item)
    return Success(msg="部门列表查询成功！", data=data)


@departRouter.post("/update", summary="修改部门信息")
async def update_depart(data: DepartUpdate):
    result = await departController.update(data.id, data)
    data = await result.to_dict()
    logger.success(f"部门更新成功！{data}")
    return Success(msg="部门更新成功！", data=data)
