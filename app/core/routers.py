from app.api.v1.user.auth import auth_router
from fastapi import APIRouter


api_routers = APIRouter(prefix='/api/v1')

api_routers.include_router(auth_router, tags=['用户管理'])
