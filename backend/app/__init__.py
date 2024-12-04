from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.exceptions import SettingNotFound
from app.core.init_app import (
    make_middlewares,
    register_exceptions,
    register_routers,
)
from app.core.init_db import init_db

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
    static_path = Path.joinpath(Path(__file__).parent, "static")
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    return app


app = create_app()


@app.on_event("startup")
async def startup_event():
    await init_db(app)
