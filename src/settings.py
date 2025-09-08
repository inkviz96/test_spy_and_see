# type: ignore
from pydantic import Field
from pydantic_settings import BaseSettings


class BaseEnvSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


class PostgresSettings(BaseEnvSettings):
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")


class RedisSettings(BaseEnvSettings):
    REDIS_HOST: str = Field(..., env="REDIS_HOST")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    REDIS_DB: int = Field(..., env="REDIS_DB")
    REDIS_PASSWORD: str = Field(..., env="REDIS_PASSWORD")
    REDIS_SSL: bool = Field(..., env="REDIS_SSL")


class Settings(BaseEnvSettings):
    DEBUG: bool = Field(default=True, env="DEBUG")
    DEBUG_PORT: int = Field(default=8080, env="DEBUG_PORT")
    OPENAPI_URL: str = Field(default="/openapi.json", env="OPENAPI_URL")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24, env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24 * 7, env="REFRESH_TOKEN_EXPIRE_MINUTES"
    )


settings = Settings()
redis_settings = RedisSettings()
postgres_settings = PostgresSettings()
