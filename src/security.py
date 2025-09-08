# type: ignore
import base64
from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from services.authorization.authorization import TokenType, token_whitelist_service
from services.authorization.exceptions import TokenHTTPException
from services.authorization.schemas import Token, TypeOfToken
from settings import settings


def get_expiration_time(delta: timedelta | None = None) -> datetime:
    """Get expiration time.

    Args:
        delta: Time delta to expire.

    Returns:
        datetime: Expire datetime.
    """
    return (
        datetime.utcnow() + delta
        if delta
        else datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def decode_private_public_key_for_jwt(encoded_key: str):
    """Decode private key and public key.

    Args:
        encoded_key: Encoded key.

    Returns:
        str: Decoded key.
    """
    return base64.b64decode(encoded_key).decode("utf-8")


async def create_access_token(
    username: str, delta: timedelta = None, is_refresh: bool = False
) -> str:
    """Create access token.

    Args:
        username: User name.
        delta: Time delta to expire.
        is_refresh: Is refresh token.

    Returns:
        str: Access token.
    """
    expiration_time = get_expiration_time(delta=delta)
    refresh_token_expiration_in_seconds = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    access_token_expiration_in_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60

    token = jwt.encode(
        claims=Token(
            sub=username,
            exp=expiration_time,
            type=TypeOfToken.refresh if is_refresh else TypeOfToken.access,
        ).model_dump(),
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    await token_whitelist_service.add(
        token=token,
        username=username,
        expiration_time=refresh_token_expiration_in_seconds
        if is_refresh
        else access_token_expiration_in_seconds,
        token_type=TokenType.REFRESH if is_refresh else TokenType.ACCESS,
    )

    return token


def decode_token(token: str) -> dict[str, Any]:
    """Decode JWT token.

    Args:
        token: JWT token.

    Returns:
        dict[str, Any]: Decoded token.
    """
    return jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )


def get_token_data(token: str) -> Token:
    """Get token data.

    Args:
        token: JWT token.

    Returns:
        Token: Token data.

    Raises:
        WrongCredentialsHTTPException: If token is invalid.
    """
    try:
        payload = decode_token(token=token)
    except JWTError:  # noqa: WPS329
        raise TokenHTTPException("Token is not in the whitelist")
    username = payload.get("sub")
    if username is None:
        raise TokenHTTPException("Token is not in the whitelist")

    return Token(sub=username, exp=payload.get("exp"), type=payload.get("type"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password.

    Args:
        plain_password: Plain password.
        hashed_password: Hashed password.

    Returns:
        bool: True if password is correct, False otherwise.
    """
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get password hash.

    Args:
        password: Password.

    Returns:
        str: Password hash.
    """
    return pbkdf2_sha256.hash(password)
