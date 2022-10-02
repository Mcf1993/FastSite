from pydantic import BaseModel


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
    password: str
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str

