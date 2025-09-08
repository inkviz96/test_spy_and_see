from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from base_model import BaseModel


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="notifications")
    type = Column(String(15), nullable=False)
    text = Column(String(255), nullable=False)
