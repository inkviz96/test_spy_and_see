from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from base_model import BaseModel
from consts import DEFAULT_AVATAR_URL


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    avatar_url = Column(String, nullable=False, default=DEFAULT_AVATAR_URL)

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
