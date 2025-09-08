from math import ceil

from fastapi import APIRouter, Depends, status

from dependencies import get_current_user, get_notification_repository
from notifications.repostiory import NotificationRepository
from notifications.schemas import (
    NotificationDeleteSchema,
    NotificationPagginateSchema,
    NotificationSchema,
)
from users.schemas import UserSchema

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationSchema,
    notification_repository: NotificationRepository = Depends(
        get_notification_repository
    ),
    current_user: UserSchema = Depends(get_current_user),
):
    notification_data.user_id = current_user.id
    notification_repository.add(notification_data)


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=NotificationPagginateSchema
)
async def get_user_notifications(
    page: int = 1,
    current_user: UserSchema = Depends(get_current_user),
    notification_repository: NotificationRepository = Depends(
        get_notification_repository
    ),
):
    if page < 1:
        page = 1

    offset = (page - 1) * 5
    notifications = notification_repository.find_with_pagging(
        offset=offset, user_id=current_user.id
    )
    total_pages = ceil(len(notifications) / 5)
    return NotificationPagginateSchema(
        items=notifications,
        pages=total_pages,
        current_page=page,
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_notification(
    notification_id: NotificationDeleteSchema,
    current_user: UserSchema = Depends(get_current_user),
    notification_repository: NotificationRepository = Depends(
        get_notification_repository
    ),
):
    notification = notification_repository.find(
        user_id=current_user.id, id=notification_id.id
    )
    if notification:
        notification_repository.delete(notification_id=notification.id)
