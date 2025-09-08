import logging
from enum import StrEnum

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from services.redis import redis_service


class HealthCheckStatus(StrEnum):
    """Health check status."""

    OK = "ok"
    FAIL = "fail"


class HealthCheckResponse(BaseModel):
    database: HealthCheckStatus
    redis: HealthCheckStatus


def get_health_check_status_for_database(db: Session) -> HealthCheckStatus:
    """Get health check status for database.

    Args:
        db: Database session.

    Returns:
        HealthCheckStatus: Health check status.

    Raises:
        Exception: If database health check failed.
    """
    try:
        db.execute(text("SELECT 1"))
        return HealthCheckStatus.OK
    except Exception as error:  # pragma: no cover
        logging.debug(f"Database health check failed with error: {error}")
        return HealthCheckStatus.FAIL


async def get_health_check_status_for_redis() -> HealthCheckStatus:
    """Get health check status for redis.

    Returns:
        HealthCheckStatus: Health check status.

    Raises:
        Exception: If redis health check failed.
    """
    try:
        if await redis_service.ping():
            return HealthCheckStatus.OK
        return HealthCheckStatus.FAIL
    except Exception as error:  # pragma: no cover
        logging.debug(f"Redis health check failed with error: {error}")
        return HealthCheckStatus.FAIL
