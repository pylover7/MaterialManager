from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import Menu

MenuPydantic = pydantic_model_creator(Menu)


class MenuCreate(MenuPydantic):
    ...


class MenuUpdate(MenuPydantic):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


if __name__ == '__main__':
    print(MenuPydantic.schema_json())
