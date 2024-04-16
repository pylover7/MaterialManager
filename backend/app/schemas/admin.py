# coding=utf-8
# @FileName  :admin.py
# @Time      :2024/4/16 下午9:29
# @Author    :dayezi
from pydantic import BaseModel, Field


class DbInfo(BaseModel):
    db_start: str = Field(..., description="数据库启动类型")
    db_name: str = Field(..., description="数据库名称")
    db_host: str = Field(..., description="数据库地址")
    db_port: int = Field(3306, description="数据库端口")
    db_user: str = Field(..., description="数据库用户名")
    db_password: str = Field(..., description="数据库密码")
