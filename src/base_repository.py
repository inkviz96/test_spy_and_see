from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

EntityT = TypeVar("EntityT", bound=BaseModel)


class BaseRepository(ABC, Generic[EntityT]):
    def __init__(self, db: Session):
        self._db = db
        self.objects = self._db

    @abstractmethod
    def get(self, entity_id: int) -> EntityT:
        """Get an entity by id.

        Args:
            entity_id: Entity id.

        Returns:
            EntityT: Entity.
        """

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Delete an entity by id.

        Args:
            entity_id: Entity id.
        """

    @abstractmethod
    def update(self, entity: EntityT) -> EntityT:
        """Update an entity by id.

        Args:
            entity: Entity data.

        Returns:
            EntityT: Entity.
        """

    @abstractmethod
    def add(self, entity: EntityT) -> EntityT:
        """Add an entity.

        Args:
            entity: Entity data.

        Returns:
            EntityT: Entity.
        """

    @abstractmethod
    def find(self, **kwargs) -> EntityT:
        """Find an entity.

        Args:
            kwargs: Filters data.

        Returns:
            EntityT: Entity.
        """
