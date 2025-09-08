from sqlalchemy.exc import NoResultFound

from base_repository import BaseRepository
from notifications.models import Notification
from notifications.schemas import NotificationSchema


class NotificationRepository(BaseRepository[NotificationSchema]):
    def get(self, notification_id: int) -> NotificationSchema:
        """Get a notification by id.

        Args:
            notification_id: Notification id.

        Returns:
            Notification: Notification.

        Raises:
            NoResultFound: If notification not found.
        """
        notification = (
            self._db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )

        if not notification:
            raise NoResultFound("Notification not found")

        return NotificationSchema.model_validate(notification)

    def delete(self, notification_id: int) -> None:
        """Delete a notification by id.

        Args:
            user_uuid: Notification id.
        """
        self._db.query(Notification).filter(Notification.id == notification_id).delete()
        self._db.commit()

    def update(self, notification: NotificationSchema) -> NotificationSchema:
        """Update a notification by id.

        Args:
            notification: Notification data.

        Returns:
            Notification: NotificationSchema.
        """
        self._db.query(Notification).filter(Notification.id == notification.id).update(
            values=notification.model_dump(exclude_unset=True),
        )  # noqa: WPS221
        self._db.commit()

        notification = (
            self._db.query(Notification)
            .filter(Notification.id == notification.id)
            .first()
        )

        if not notification:
            raise NoResultFound("Notification not found")

        return notification

    def add(self, notification: NotificationSchema) -> NotificationSchema:
        """Add a notification.

        Args:
            notification: Notification data.

        Returns:
            Notification: Notification.
        """
        notification = Notification(**notification.model_dump(exclude_unset=True))
        self._db.add(notification)
        self._db.commit()

        return NotificationSchema.model_validate(notification)

    def find(self, **kwargs) -> NotificationSchema:
        """Find a notification.

        Args:
            kwargs: Filters data.

        Returns:
            Notification: Notification.
        """
        notification = self._db.query(Notification).filter_by(**kwargs).first()
        if notification:
            return NotificationSchema.model_validate(notification)

    def find_with_pagging(self, offset: int = 1, **kwargs) -> list[NotificationSchema]:
        """Find a notification.

        Args:
            offset: page number,
            kwargs: Filters data.

        Returns:
            Notification: Notification.
        """
        notifications = (
            self._db.query(Notification)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(5)
            .all()
        )
        if notifications:
            return [
                NotificationSchema.model_validate(notification)
                for notification in notifications
            ]
        return []
