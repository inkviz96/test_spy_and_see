from datetime import timedelta

from fastapi import APIRouter, Depends, Request, status

from dependencies import get_current_user_by_refresh_token, get_user_repository
from security import create_access_token, verify_password
from settings import settings
from users.exceptions import (
    UserAlreadyExistsHTTPException,
    WrongCredentialsOrUserNotFoundHTTPException,
)
from users.repository import UserRepository
from users.schemas import (
    LoginResponse,
    LoginSchema,
    RefreshTokenResponse,
    RegisterResponse,
    UserSchema,
)

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_200_OK, response_model=RegisterResponse
)
async def register(
    user_data: UserSchema,
    user_repository: UserRepository = Depends(get_user_repository),
):
    user = user_repository.find(username=user_data.username)
    print(user, flush=True)
    if user:
        raise UserAlreadyExistsHTTPException(
            f"user with {user_data.username=} already exists"
        )
    user = user_repository.add(user=user_data)
    return RegisterResponse(
        access=await create_access_token(
            username=user.username,
            delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            is_refresh=False,
        ),
        refresh=await create_access_token(
            username=user.username,
            delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            is_refresh=True,
        ),
        user_id=user.id,
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def login(  # noqa: WPS217
    request: Request,
    login_data: LoginSchema,
    user_repository: UserRepository = Depends(get_user_repository),
):
    """Login for OTP.

    Args:
        request: The request object.
        login_data: Login data.
        auth_service: Auth service.
        device_bind_service: Device bind service.
        auth_attempt_repository: Auth attempt repository.

    Returns:
        TokenPair: Access and refresh tokens if user second factor authentication is disabled.
        LoginOTPTypeResponse: Login OTP type response schema if user second factor authentication is enabled.

    Raises:
        WrongCredentialsHTTPException: If user does not authenticate.
        OtpRetryError: If new OTP was requested too soon.
    """
    client_ip = request.client and request.client.host
    user = user_repository.find(username=login_data.username)
    if not user:
        raise WrongCredentialsOrUserNotFoundHTTPException(
            "Could not validate credentials"
        )

    if user.password is None or not verify_password(
        plain_password=login_data.password, hashed_password=user.password
    ):
        raise WrongCredentialsOrUserNotFoundHTTPException(
            f"Wrong credentials for user: {login_data.username}, ip: {client_ip}"
        )

    return LoginResponse(
        access=await create_access_token(
            username=user.username,
            delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            is_refresh=False,
        ),
        refresh=await create_access_token(
            username=user.username,
            delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            is_refresh=True,
        ),
    )


@router.post(
    "/refresh", status_code=status.HTTP_200_OK, response_model=RefreshTokenResponse
)
async def refresh_token(
    user: UserSchema = Depends(get_current_user_by_refresh_token),
):
    """Refresh access token.

    Args:
        user: Current user from refresh token.

    Returns:
        TokenWithoutRefresh: Access token.
    """
    return RefreshTokenResponse(
        access=await create_access_token(
            username=user.username,
            delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            is_refresh=False,
        ),
    )
