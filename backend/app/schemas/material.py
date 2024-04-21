from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import Material, AttentionNote

MaterialPydantic = pydantic_model_creator(Material, name="Material")
AttentionNotePydantic = pydantic_model_creator(AttentionNote, name="AttentionNote")


class MaterialCreate(MaterialPydantic):
    ...


class MaterialUpdate(MaterialPydantic):
    ...


class AttentionNoteCreate(AttentionNotePydantic):
    ...


class AttentionNoteUpdate(AttentionNotePydantic):
    ...
