# coding=utf-8
# @FileName  :admin.py
# @Time      :2024/4/16 下午9:29
# @Author    :dayezi
from pydantic import BaseModel, Field


class DbInfo(BaseModel):
    start: str | None = Field(..., description="数据库启动类型")
    database: str | None = Field(..., description="数据库名称")
    host: str | None = Field(..., description="数据库地址")
    port: int | None = Field(3306, description="数据库端口")
    username: str | None = Field(..., description="数据库用户名")
    password: str | None = Field(..., description="数据库密码")
