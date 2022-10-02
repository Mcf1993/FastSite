from app.core.response import response
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from typing import Union


HttpStatusSelector = {
    '401': '请先进行登陆'
}


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content=response(
            code=exc.status_code,
            message=HttpStatusSelector.get(str(exc.status_code), exc.detail),
            data=[]
        )
    )


async def params_validation_handler(request: Request, exc: Union[RequestValidationError, ]) -> JSONResponse:
    return JSONResponse(
        content=response(
            code=HTTP_422_UNPROCESSABLE_ENTITY,
            message=f'数据校验错误 {exc.errors()}',
            data=[]
        )
    )
