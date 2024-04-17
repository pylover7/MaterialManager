from fastapi import FastAPI

from app.core.exceptions import SettingNotFound
from app.core.init_app import (
    make_middlewares,
    register_exceptions,
    register_routers,
)
from app.log import logger

try:
    from app.settings.config import settings
except ImportError:
    raise SettingNotFound("Can not import settings")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
    )
    register_exceptions(app)
    register_routers(app, prefix="/api")
    logger.success("应用初始化成功")
    return app


app = create_app()


# @app.on_event("startup")
# async def startup_event():
#     await init_menus()
