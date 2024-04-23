from tortoise import fields

from app.schemas.menus import MenuType

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class User(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=20, unique=True, description="用户名称")
    alias = fields.CharField(max_length=30, null=True, description="姓名")
    email = fields.CharField(max_length=255, unique=True, description="邮箱")
    phone = fields.CharField(max_length=20, null=True, description="电话")
    password = fields.CharField(max_length=128, description="密码")
    depart = fields.CharField(max_length=20, description="部门")
    is_active = fields.BooleanField(default=False, description="是否激活")
    is_superuser = fields.BooleanField(default=False, description="是否为超级管理员")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField("models.Role", related_name="user_roles")

    class Meta:
        table = "user"

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "id")


class Role(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="角色名称")
    desc = fields.CharField(max_length=500, null=True, blank=True, description="角色描述")
    menus: fields.ManyToManyRelation["Menu"] = fields.ManyToManyField("models.Menu", related_name="role_menus")
    apis: fields.ManyToManyRelation["Api"] = fields.ManyToManyField("models.Api", related_name="role_apis")

    class Meta:
        table = "role"


class Menu(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, description="菜单名称")
    remark = fields.JSONField(null=True, description="保留字段", blank=True)
    menu_type = fields.CharEnumField(MenuType, null=True, blank=True, description="菜单类型")
    icon = fields.CharField(max_length=100, null=True, blank=True, description="菜单图标")
    path = fields.CharField(max_length=100, description="菜单路径")
    order = fields.IntField(default=0, description="排序")
    parent_id = fields.IntField(default=0, max_length=10, description="父菜单ID")
    is_hidden = fields.BooleanField(default=False, description="是否隐藏")
    component = fields.CharField(max_length=100, description="组件")
    keepalive = fields.BooleanField(default=True, description="存活")
    redirect = fields.CharField(max_length=100, null=True, blank=True, description="重定向")

    class Meta:
        table = "menu"

    class PydanticMeta:
        exclude = ("created_at", "updated_at")


class Api(BaseModel, TimestampMixin):
    path = fields.CharField(max_length=100, description="API路径")
    method = fields.CharEnumField(MethodType, description="请求方法")
    summary = fields.CharField(max_length=500, description="请求简介")
    tags = fields.CharField(max_length=100, description="API标签")

    class Meta:
        table = "api"


class Depart(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="部门名称")
    parentId = fields.IntField(default=0, max_length=10, description="父部门ID")
    sort = fields.IntField(default=0, description="排序")
    phone = fields.CharField(max_length=20, null=True, description="电话")
    principal = fields.CharField(max_length=20, null=True, description="负责人")
    email = fields.CharField(max_length=255, null=True, description="邮箱")
    status = fields.IntField(default=1, description="状态：启用/停用")
    type = fields.IntField(default=0, description="部门类型：1-公司，2-处室，3-科室")
    remark = fields.CharField(max_length=500, null=True, blank=True, description="备注信息")

    class Meta:
        table = "depart"

    class PydanticMeta:
        exclude = ("id", "created_at", "updated_at")
