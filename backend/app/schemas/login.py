from datetime import datetime

from pydantic import BaseModel, Field


class CredentialsSchema(BaseModel):
    username: str = Field(..., description="用户名称", example="admin")
    password: str = Field(..., description="密码", example="admin123456")


class refreshTokenSchema(BaseModel):
    refreshToken: str = Field(..., description="刷新令牌", example="eyJhbGciOiJIUzUxMiJ9.newAdminRefresh")


class JWTReOut(BaseModel):
    accessToken: str
    refreshToken: str
    expires: str


class JWTOut(BaseModel):
    username: str
    uuid: str
    depart: str
    roles: list[str]
    accessToken: str
    refreshToken: str
    expires: str


class JWTPayload(BaseModel):
    user_id: int
    username: str
    is_superuser: bool
    exp: datetime
