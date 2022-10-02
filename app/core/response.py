from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Any


T = TypeVar('T')


class BaseResponse(GenericModel, Generic[T]):
    code: int
    message: str
    data: T


def response(code: int = 0, message: str = 'success', data: Any = []) -> BaseResponse:
    return {
        'code': code,
        'message': message,
        'data': data
    }
