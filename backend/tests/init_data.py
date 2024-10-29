# coding=utf-8
# @FileName  :init_data.py
# @Time      :2024/10/29 17:16
# @Author    :dayezi
import asyncio

import pandas as pd
from tortoise import Tortoise

from app.settings import settings
from app.schemas.users import UserCreate, DepartCreate
from app.controllers.user import user_controller
from app.controllers.depart import departController
from app.controllers.user import role_controller
from app.utils import generate_uuid
from app.utils.password import md5_encrypt

excel_file_path = "./goodsmanage_container_person.xlsx"

df = pd.read_excel(excel_file_path, header=None)
async def create_data():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

    for _, row in df.iterrows():
        company, depart, nickname, phone, username = row
        departP = await departController.get_by_name(depart)
        if departP is None:
            try:
                departP = await departController.create(DepartCreate(name=company))
            except Exception as e:
                continue
        departC = await departController.get_by_name(depart)
        if departC is None:
            try:
                departC = await departController.create(DepartCreate(name=depart, parentId=departP.id))
            except Exception as e:
                continue
        password = md5_encrypt("1")
        role = await role_controller.get(2)
        user_id = generate_uuid(username)
        # print(departC.id, user_id, nickname, phone, username, password, role)

        user = await user_controller.get_by_username(username)
        if user is None:
            try:
                user = await user_controller.create(
                    UserCreate(
                        uuid=user_id,
                        nickname=nickname,
                        phone=f"{phone}",
                        username=f"{username}",
                        password=password,
                        email=None,
                        remark=None,
                    )
                )
                print(f"用户：{user.nickname}创建成功")
            except Exception as e:
                print(e)
                continue
        user.depart = departC
        await user.roles.add(role)
        await user.save()

    await Tortoise.close_connections()

if __name__ == '__main__':
    asyncio.run(create_data())
