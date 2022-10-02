from pydantic import BaseModel


class PermissionCreate(BaseModel):
    code: str
    display_name: str


class PermissionUpdate(PermissionCreate):
    pass


class PermissionBase(PermissionCreate):
    id: int
