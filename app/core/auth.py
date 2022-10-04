from app.core.settings import settings
from app.curd.auth.user import user_curd
from datetime import datetime, timedelta
from fastapi import Depends, Request, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.param_functions import Form
from jose import jwt
from starlette import status
from passlib.context import CryptContext
from typing import Optional


oauth2 = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/user/login/', scheme_name="User",)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user_token(payload: dict):
    access_token_expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    sign_data = {
        'sub': payload.username
    }.copy()
    sign_data.update({"exp": access_token_expires})
    access_token = jwt.encode(sign_data, settings.APP_SECRET_KEY, algorithm=settings.APP_ALGORITHM)
    return access_token


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password: str):
    return pwd_context.hash(password)


class OAuth2Form(OAuth2PasswordRequestForm):
    def __init__(self,
                 grant_type: str = Form(default=None, regex="password"),
                 username: str = Form(),
                 password: str = Form(),
                 scope: str = Form(default=""),
                 client_id: Optional[str] = Form(default=None),
                 client_secret: Optional[str] = Form(default=None),
                 hash_key: str = Form(),
                 verify_code: str = Form()):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.hash_key = hash_key
        self.verify_code = verify_code


async def authenticate_user(request: Request, token=Depends(oauth2)):
    try:
        payload = jwt.decode(
            token,
            settings.APP_SECRET_KEY,
            algorithms=[settings.APP_ALGORITHM]
        )
        user_instance = user_curd.get_user_instance_by_username(request.state.db, payload.get('sub'))
        if user_instance is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效凭证",
                headers={"WWW-Authenticate": f"Bearer {token}"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
