from tortoise import fields

from .base import BaseModel, TimestampMixin, UUIDModel


class Material(BaseModel, TimestampMixin, UUIDModel):
    name = fields.CharField(max_length=50, description="物资名字")
    model = fields.CharField(max_length=20, null=True, description="物资型号")
    position = fields.CharField(max_length=50, description="物资位置")
    number = fields.IntField(description="物资数量")
    depart = fields.CharField(max_length=20, description="物资所属部门")

    class Meta:
        table = "material"

    class PydanticMeta:
        exclude = ("id", "uuid", "created_at", "updated_at")


class AttentionNote(BaseModel, TimestampMixin, UUIDModel):
    note = fields.CharField(max_length=255, description="事项")
    depart = fields.CharField(max_length=20, description="所属部门")

    class Meta:
        table = "attention_note"

    class PydanticMeta:
        exclude = ("id", "uuid", "created_at", "updated_at")
