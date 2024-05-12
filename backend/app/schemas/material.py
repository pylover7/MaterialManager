from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Material, AttentionNote, DutyOverList

MaterialPydantic = pydantic_model_creator(Material)
AttentionNotePydantic = pydantic_model_creator(AttentionNote)
DutyOverListPydantic = pydantic_model_creator(DutyOverList)


class MaterialCreate(MaterialPydantic):
    ...


class MaterialUpdate(MaterialPydantic):
    id: int


class AttentionNoteCreate(AttentionNotePydantic):
    ...


class AttentionNoteUpdate(AttentionNotePydantic):
    id: int


class DutyOverListCreate(DutyOverListPydantic):
    ...


class DutyOverListUpdate(DutyOverListPydantic):
    id: int
