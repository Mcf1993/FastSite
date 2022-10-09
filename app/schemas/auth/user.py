from pydantic import BaseModel, Field


class UserInstance(BaseModel):
    id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    email: str
    full_name: str


class UserCreate(BaseModel):
    username: str
    password: str
    email: str


class UserRegister(BaseModel):
    username: str
    password: str = Field(
        min_length=6,
        max_length=32
    )
    confirm_password: str = Field(
        min_length=6,
        max_length=32,
    )
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class CaptchaResponse(BaseModel):
    hash_key: str
    image_base64: str

