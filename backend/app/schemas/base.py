from typing import Any, Optional

from fastapi.responses import JSONResponse


class Success(JSONResponse):
    def __init__(
        self,
        code: int = 200,
        msg: Optional[str] = "OK",
        data: Optional[Any] = None,
        **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


class Fail(JSONResponse):
    def __init__(
        self,
        code: int = 400,
        msg: Optional[str] = "Fail",
        data: Optional[Any] = None,
        **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


class SuccessExtra(JSONResponse):
    def __init__(
        self,
        code: int = 200,
        msg: Optional[str] = "OK",
        data: Optional[Any] = None,
        total: int = 0,
        currentPage: int = 1,
        pageSize: int = 20,
        **kwargs,
    ):
        content = {
            "code": code,
            "msg": msg,
            "data": data,
            "total": total,
            "currentPage": currentPage,
            "pageSize": pageSize,
        }
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


class FailAuth(JSONResponse):
    def __init__(
            self,
            code: int = 401,
            msg: Optional[str] = "Unauthorized",
            **kwargs,
    ):
        content = {"code": code, "msg": msg}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)
