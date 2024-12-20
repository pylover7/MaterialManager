from tortoise import fields

from .area import MaterialArea
from .base import BaseModel, TimestampMixin, UUIDModel
from .enums import MethodType
from .borrowed import Borrowed


class User(BaseModel, TimestampMixin, UUIDModel):
    username = fields.CharField(max_length=20, unique=True, description="用户唯一标识")
    nickname = fields.CharField(max_length=30, description="用户名字")
    employeeID = fields.CharField(max_length=20, unique=True, description="员工工号")
    avatar = fields.CharField(max_length=255, null=True, description="头像文件名称")
    sex = fields.IntField(default=1, description="性别, 0: 女, 1: 男")
    email = fields.CharField(max_length=255, null=True, unique=True, description="邮箱")
    mobile = fields.CharField(max_length=20, null=True, unique=True, description="手机号码")
    status = fields.IntField(default=1, max_length=10, description="是否禁用")
    is_superuser = fields.BooleanField(default=False, description="是否为超级管理员")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    remark = fields.CharField(max_length=500, null=True, blank=True, description="备注")
    department = fields.CharField(max_length=500, null=True, blank=True, description="部门")
    company = fields.CharField(max_length=500, null=True, blank=True, description="公司")
    loginFail = fields.IntField(default=0, description="登录失败次数")

    roles: fields.ManyToManyRelation["Role"] = fields.ManyToManyField("models.Role", related_name="user_roles")
    borrowed: fields.ManyToManyRelation["Borrowed"]

    class Meta:
        table = "user"

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "id")


class Role(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="角色名称")
    code = fields.CharField(max_length=20, unique=True, description="角色编码")
    status = fields.IntField(default=0, description="状态：启用/停用")
    default = fields.IntField(default=0, description="是否为默认角色")
    remark = fields.CharField(max_length=500, null=True, blank=True, description="角色描述")

    menus: fields.ManyToManyRelation["Menu"] = fields.ManyToManyField("models.Menu", related_name="roles")
    apis: fields.ManyToManyRelation["Api"] = fields.ManyToManyField("models.Api", related_name="roles")
    users: fields.ManyToManyRelation["User"]
    areas: fields.ManyToManyRelation["MaterialArea"] = fields.ManyToManyField("models.MaterialArea", related_name="roles")

    class Meta:
        table = "role"

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "id")


class Menu(BaseModel, TimestampMixin):
    parentId = fields.IntField(default=0, max_length=10, description="父菜单ID")
    menuType = fields.IntField(default=0, max_length=10, description="菜单类型（0代表菜单、1代表iframe、2代表外链、3代表按钮）")
    title = fields.CharField(max_length=20, description="菜单名称")
    name = fields.CharField(max_length=50, description="路由名称必须唯一")
    path = fields.CharField(max_length=100, description="菜单路径")
    component = fields.CharField(max_length=100, null=True, description="组件")
    rank = fields.IntField(default=1, description="排序")
    redirect = fields.CharField(max_length=100, null=True, blank=True, description="重定向")
    icon = fields.CharField(max_length=100, null=True, blank=True, description="菜单图标")
    extraIcon = fields.CharField(max_length=100, null=True, blank=True, description="右侧图标")
    transitionName = fields.CharField(max_length=100, null=True, blank=True, description="当前页面动画")
    enterTransition = fields.CharField(max_length=100, null=True, blank=True, description="进入动画")
    leaveTransition = fields.CharField(max_length=100, null=True, blank=True, description="离开动画")
    dynamicLevel = fields.IntField(default=1, description="显示在标签页的最大数量")
    activePath = fields.CharField(max_length=100, null=True, blank=True, description="菜单激活")
    auths = fields.CharField(max_length=100, null=True, description="权限标识")
    frameSrc = fields.CharField(max_length=100, null=True, blank=True, description="iframe地址")
    frameLoading = fields.BooleanField(default=True, description="iframe加载动画")
    keepAlive = fields.BooleanField(default=False, description="缓存页面")
    hiddenTag = fields.BooleanField(default=False, description="标签页")
    fixedTag = fields.BooleanField(default=False, description="固定标签")
    showLink = fields.BooleanField(default=True, description="显示链接")
    showParent = fields.BooleanField(default=False, description="显示父菜单")

    roles: fields.ManyToManyRelation["Role"]

    class Meta:
        table = "menu"

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "id")


class Api(BaseModel, TimestampMixin):
    path = fields.CharField(max_length=100, description="API路径")
    method = fields.CharEnumField(MethodType, description="请求方法")
    summary = fields.CharField(max_length=500, description="请求简介")
    tags = fields.CharField(max_length=100, description="API标签")

    class Meta:
        table = "api"