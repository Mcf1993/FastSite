from app.curd.base import CURDBase
from app.models.user import Permission
from app.schemas.auth.permission import PermissionBase, PermissionCreate, PermissionUpdate


class PermissionCURD(CURDBase[PermissionBase, PermissionCreate, PermissionUpdate]):
    pass


permissionCURD = PermissionCURD(Permission)

