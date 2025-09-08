import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import postgres_settings

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)


SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://"
    f"{postgres_settings.POSTGRES_USER}:{postgres_settings.POSTGRES_PASSWORD}@"
    f"{postgres_settings.POSTGRES_HOST}:{postgres_settings.POSTGRES_PORT}/"
    f"{postgres_settings.POSTGRES_DB}"
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=0,
    max_overflow=-1,
    pool_timeout=10,
    pool_recycle=3600,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Get a database session.

    Yields:
        The database session
    """
    with SessionLocal() as db:  # pragma: no cover
        try:
            yield db  # pragma: no cover
        finally:
            db.close()
