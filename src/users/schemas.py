from typing import Optional

from base_schema import BaseSchema


class UserSchema(BaseSchema):
    id: Optional[int] = None
    username: str
    avatar_url: Optional[str] = None
    password: str


class LoginSchema(BaseSchema):
    username: str
    password: str


class LoginResponse(BaseSchema):
    access: str
    refresh: str


class RegisterResponse(LoginResponse):
    user_id: int


class RefreshTokenResponse(BaseSchema):
    access: str
