from datetime import datetime
from enum import Enum
from typing import Optional

from base_schema import BaseSchema, Pagginate


class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class NotificationSchema(BaseSchema):
    id: Optional[int] = None
    user_id: Optional[int] = None
    type: NotificationType
    text: str
    created_at: Optional[datetime] = None


class NotificationPagginateSchema(Pagginate):
    items: list[NotificationSchema] = []


class NotificationDeleteSchema(BaseSchema):
    id: int
