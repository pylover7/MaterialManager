from tortoise import fields

from .base import BaseModel, TimestampMixin, UUIDModel
from .borrowed import Borrowed


class Material(BaseModel, TimestampMixin, UUIDModel):
    type = fields.CharField(max_length=20, description="物资类型")
    area = fields.CharField(max_length=20, description="物资所属区域")
    name = fields.CharField(max_length=50, description="物资名称")
    code = fields.CharField(max_length=20, null=True, description="物资编号")
    model = fields.CharField(max_length=20, null=True, description="物资型号")
    position = fields.CharField(max_length=50, description="物资位置")
    number = fields.IntField(description="物资库存数量")
    checking = fields.IntField(default=0, description="物资送检数量")
    borrowed = fields.IntField(default=0, description="物资外借数量")
    description = fields.CharField(max_length=255, null=True, description="物资描述")

    # 物资被借的信息
    borrowedInfo: fields.ManyToManyRelation["Borrowed"]

    class Meta:
        table = "material"

    class PydanticMeta:
        exclude = ("id", "uuid", "created_at", "updated_at")


class AttentionNote(BaseModel, TimestampMixin, UUIDModel):
    note = fields.CharField(max_length=255, description="事项")
    area = fields.CharField(max_length=20, description="所属区域")

    class Meta:
        table = "attention_note"

    class PydanticMeta:
        exclude = ("id", "uuid", "created_at", "updated_at")


class DutyOverList(BaseModel, TimestampMixin):
    area = fields.CharField(max_length=20, description="部门")
    content = fields.CharField(max_length=255, description="交接班清单内容")

    class Meta:
        table = "duty_over_list"

    class PydanticMeta:
        exclude = ("id", "created_at", "updated_at")
