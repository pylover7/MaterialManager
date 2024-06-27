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
            if field == "password":
                continue
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
                        value.update((k, str(v)) for k, v in value.items() if isinstance(v, UUID))
                        value.pop("password", "xxx")  # 删除用户模型中的密码字段
                    d[field] = values
        return d

    class Meta:
        abstract = True


class UUIDModel:
    uuid = fields.UUIDField(unique=True, pk=False)


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
