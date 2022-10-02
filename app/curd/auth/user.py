from app.curd.base import CURDBase
from app.models.user import User
from app.schemas.auth.user import UserInstance, UserUpdate, UserCreate
from sqlalchemy.orm import Session


class UserCURD(CURDBase[UserInstance, UserCreate, UserUpdate]):
    def get_user_instance_by_username(self, db: Session, username: str) -> UserInstance:
        return db.query(self.model).filter(self.model.username == username).first()

    def get_user_instance_by_email(self, db: Session, email: str) -> UserInstance:
        return db.query(self.model).filter(self.model.email == email).first()


user_curd = UserCURD(User)
