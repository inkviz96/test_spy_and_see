from sqlalchemy.exc import NoResultFound

from base_repository import BaseRepository
from security import get_password_hash
from users.models import User as UserORM
from users.schemas import UserSchema


class UserRepository(BaseRepository[UserSchema]):
    def get(self, user_id: int) -> UserSchema:
        """Get a user by id.

        Args:
            user_uuid: User id.

        Returns:
            User: User.

        Raises:
            NoResultFound: If user not found.
        """
        user = self._db.query(UserORM).filter(UserORM.id == user_id).first()

        if not user:
            raise NoResultFound("User not found")

        return UserSchema.model_validate(user)

    def delete(self, user_id: int) -> None:
        """Delete a user by id.

        Args:
            user_uuid: User id.
        """
        self._db.query(UserORM).filter(UserORM.id == user_id).delete()

    def update(self, user: UserSchema) -> UserSchema:
        """Update a user by id.

        Args:
            user: User data.

        Returns:
            User: UserUpdate.
        """
        self._db.query(UserORM).filter(UserORM.id == user.id).update(
            values=user.model_dump(exclude_unset=True),
        )  # noqa: WPS221
        self._db.commit()

        user = self._db.query(UserORM).filter(UserORM.id == user.id).first()

        if not user:
            raise NoResultFound("User not found")

        return user

    def add(self, user: UserSchema) -> UserSchema:
        """Add a user.

        Args:
            user: User data.

        Returns:
            User: User.
        """
        user.password = get_password_hash(user.password)
        user = UserORM(**user.model_dump(exclude_unset=True))
        self._db.add(user)
        self._db.commit()

        return UserSchema.model_validate(user)

    def find(self, **kwargs) -> UserSchema:
        """Find a user.

        Args:
            kwargs: Filters data.

        Returns:
            User: User.
        """
        user_data = self._db.query(UserORM).filter_by(**kwargs).first()
        if user_data:
            return UserSchema.model_validate(user_data)
