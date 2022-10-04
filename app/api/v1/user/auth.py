from app.core.auth import create_user_token, authenticate_user, password_hash, verify_password
from app.core.response import response, BaseResponse
from app.curd.auth.permission import permissionCURD
from app.curd.auth.user import user_curd
from app.libs.image_captcha import ImageCaptchaCls
from app.schemas.auth.user import UserInstance, UserRegister, UserCreate, LoginResponse, CaptchaResponse
from app.schemas.auth.permission import PermissionBase
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Security
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from typing import List

auth_router = APIRouter(prefix='/auth')


@auth_router.get('get/user/list/', summary="获取所有会员列表", response_model=BaseResponse[List[UserInstance]],
                 dependencies=[Security(authenticate_user, )])
async def get_user_list(request: Request):
    user_list = user_curd.get_all(request.state.db)
    return response(data=jsonable_encoder(user_list))


@auth_router.get('/user/{user_id}/', summary='获取会员实例', response_model=BaseResponse[UserInstance],
                 dependencies=[Security(authenticate_user, )])
async def get_user_instance(request: Request, user_id: int):
    user_instance = user_curd.get(request.state.db, user_id)
    return response(data=jsonable_encoder(user_instance))


@auth_router.post('/user/login/', summary="用户登录", response_model=LoginResponse)
async def user_login(request: Request, payload: OAuth2PasswordRequestForm = Depends()):
    user_instance = user_curd.get_user_instance_by_username(request.state.db, payload.username)
    if user_instance is None:
        return response(code=4004, message="用户未注册")
    if not verify_password(payload.password, user_instance.password):
        return response(code=4024, message="密码错误")
    return {"access_token": create_user_token(payload), "token_type": "bearer"}


@auth_router.post('/user/register/', summary='会员注册', response_model=BaseResponse)
async def user_register(request: Request, payload: UserRegister):
    user_instance = user_curd.get_user_instance_by_username(request.state.db, payload.username)
    if user_instance is not None:
        return response(code=4022, message="该用户名已被注册")
    user_instance = user_curd.get_user_instance_by_email(request.state.db, payload.email)
    if user_instance is not None:
        return response(code=4023, message="该邮箱已被注册")
    user_create = UserCreate(
        username=payload.username,
        password=password_hash(payload.password),
        email=payload.email,
        is_active=True,
        create_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        full_name=''
    )
    user_curd.create(request.state.db, user_create)
    return response()


@auth_router.get('/permission/list/', summary="获取所有权限", response_model=BaseResponse[List[PermissionBase]],
                 dependencies=[Security(authenticate_user, )])
async def get_permission_list(request: Request):
    all_permission = permissionCURD.get_all(request.state.db)
    return response(data=jsonable_encoder(all_permission))


@auth_router.get('/captcha/', summary="获取验证码", response_model=BaseResponse[CaptchaResponse])
async def get_captcha_img():
    hash_key, image_base64 = ImageCaptchaCls().generate_image()
    return response(data={
        'hash_key': hash_key,
        'image_base64': image_base64
    })
