from fastapi import APIRouter

from app.core.dependency import DependPermission

from .base import baseRouter
from .material import materialRouter
from .admin import adminRouter
from .home import homeRouter
from .duty import dutyRouter

v1_router = APIRouter()

v1_router.include_router(baseRouter, prefix="/base")
v1_router.include_router(homeRouter, prefix="/home", dependencies=[DependPermission])
v1_router.include_router(materialRouter, prefix="/material", dependencies=[DependPermission])
v1_router.include_router(adminRouter, prefix="/admin", dependencies=[DependPermission])
v1_router.include_router(dutyRouter, prefix="/duty", dependencies=[DependPermission])
