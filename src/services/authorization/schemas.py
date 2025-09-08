from datetime import datetime
from enum import Enum

from base_schema import BaseSchema


class TokenPair(BaseSchema):
    access_token: str
    refresh_token: str | None = None


class TypeOfToken(str, Enum):
    access = "access"
    refresh = "refresh"


class Token(BaseSchema):
    sub: str
    exp: datetime
    type: TypeOfToken | None
