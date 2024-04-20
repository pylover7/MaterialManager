from fastapi import APIRouter

from app.core.dependency import DependPermission, DependAuth

from .apis import apis_router
from .base import base_router
from .menus import menus_router
from .roles import roles_router
from .users import users_router
from .material import material_router
from .admin import admin_router

v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermission])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermission])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermission])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermission])
v1_router.include_router(material_router, prefix="/material", dependencies=[DependPermission])
v1_router.include_router(admin_router, prefix="/admin",  dependencies=[DependAuth])
