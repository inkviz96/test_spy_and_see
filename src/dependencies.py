from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from database import get_db
from exceptions import WrongCredentialsHTTPException
from notifications.repostiory import NotificationRepository
from security import get_token_data
from services.authorization.authorization import token_whitelist_service
from services.authorization.exceptions import TokenHTTPException
from services.authorization.schemas import TypeOfToken
from users.repository import UserRepository
from users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Get user repository.

    Args:
        db: Database session.

    Returns:
        UserRepository: User repository.
    """
    return UserRepository(db=db)


def get_notification_repository(
    db: Session = Depends(get_db),
) -> NotificationRepository:
    """Get notification repository.

    Args:
        db: Database session.

    Returns:
        NotificationRepository: Notification repository.
    """
    return NotificationRepository(db=db)


async def get_current_user_by_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserSchema:
    """Get current user.

    Args:
        token: JWT token.
        user_repository: User repository.

    Returns:
        User: Current user.

    Raises:
        WrongCredentialsHTTPException: If user does not exist.
        TokenIsNotInWhiteListHTTPException: If token is not on whitelist.
    """
    token_data = get_token_data(token=token)
    if token_data.type != TypeOfToken.refresh:
        raise WrongCredentialsHTTPException("Could not validate credentials")
    try:
        user = user_repository.find(username=token_data.sub)
    except NoResultFound:
        raise WrongCredentialsHTTPException("Could not validate credentials")

    if await token_whitelist_service.check_token_on_the_whitelist(
        token=token, username=user.username
    ):
        return user

    raise TokenHTTPException("Token is not in the whitelist")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserSchema:
    """Get current user.

    Args:
        token: JWT token.
        user_repository: User repository.

    Returns:
        User: Current user.

    Raises:
        WrongCredentialsHTTPException: If user does not exist.
        TokenIsNotInWhiteListHTTPException: If token is not on whitelist.
    """
    token_data = get_token_data(token=token)
    if token_data.type != TypeOfToken.access:
        raise WrongCredentialsHTTPException("Could not validate credentials")
    try:
        user = user_repository.find(username=token_data.sub)
    except NoResultFound:
        raise WrongCredentialsHTTPException("Could not validate credentials")

    if await token_whitelist_service.check_token_on_the_whitelist(
        token=token, username=user.username
    ):
        return user

    raise TokenHTTPException("Token is not in the whitelist")
