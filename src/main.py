import uvicorn
from fastapi import Depends, FastAPI, Response, status
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from database import get_db
from notifications.routers import router as notification_router
from settings import settings
from users.routers import router as auth_rounter
from utils import (
    HealthCheckResponse,
    HealthCheckStatus,
    get_health_check_status_for_database,
    get_health_check_status_for_redis,
)

app = FastAPI(openapi_url=settings.OPENAPI_URL, title="Test Spy and See")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_rounter, prefix="/auth", tags=["Auth"])
app.include_router(notification_router, prefix="/notifications", tags=["Notification"])


@app.get("/health", response_model=HealthCheckResponse, status_code=status.HTTP_200_OK)
async def healthcheck(response: Response, db: Session = Depends(get_db)):
    """
    Health check endpoint.

    Args:
        response: The response object
        db: The database session

    Returns:
        A JSON object with a status key and value of "ok"
    """
    database_status = get_health_check_status_for_database(db=db)
    redis_status = await get_health_check_status_for_redis()
    if (
        database_status == HealthCheckStatus.FAIL
        or redis_status == HealthCheckStatus.FAIL
    ):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthCheckResponse(
        database=database_status,
        redis=redis_status,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=settings.DEBUG_PORT)
