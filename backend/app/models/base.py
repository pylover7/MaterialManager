from datetime import datetime
from uuid import UUID

from tortoise import fields, models

from app.settings import settings


class BaseModel(models.Model):
    id = fields.BigIntField(pk=True, index=True)

    async def to_dict(self, m2m: bool = False, exclude_fields: list[str] | None = None):
        if exclude_fields is None:
            exclude_fields = []

        d = {}
        for field in self._meta.db_fields:
            if field not in exclude_fields:
                value = getattr(self, field)
                if isinstance(value, datetime):
                    value = value.strftime(settings.DATETIME_FORMAT)
                if isinstance(value, UUID):
                    value = str(value)
                d[field] = value
        if m2m:
            for field in self._meta.m2m_fields:
                if field not in exclude_fields:
                    values = [value for value in await getattr(self, field).all().values()]
                    for value in values:
                        value.update(
                            (k, v.strftime(settings.DATETIME_FORMAT))
                            for k, v in value.items()
                            if isinstance(v, datetime)
                        )
                    d[field] = values
        return d

    class Meta:
        abstract = True


class UUIDModel:
    uuid = fields.UUIDField(unique=True, pk=False)


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    
class Material(BaseModel, TimestampMixin, UUIDModel):
  name = fields.CharField(max_length=100, unique=True, description="物资名字")
  model = fields.CharField(max_length=100, null=True, description="物资型号")
  position = fields.CharField(max_length=100, description="物资位置")
  number = fields.CharField(max_length=100, description="物资数量")
