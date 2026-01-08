"""Configuration settings for vorpal-core."""

from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="VORPAL_",
        case_sensitive=False,
    )

    # Application
    app_name: str = "vorpal-core"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    # Database
    database_url: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://vorpal:vorpal@localhost:5432/vorpal"
    )
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Redis (optional)
    redis_url: RedisDsn | None = None

    # Authentication
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # API Keys
    api_key_prefix: str = "vp_sk_"

    # CORS
    cors_origins: list[str] = ["*"]

    # Logging
    log_level: str = "INFO"
    log_format: Literal["json", "console"] = "console"

    # OpenTelemetry
    otel_enabled: bool = False
    otel_service_name: str = "vorpal-core"
    otel_exporter_endpoint: str | None = None

    @field_validator("database_url", mode="before")
    @classmethod
    def validate_database_url(cls, v: str | PostgresDsn) -> PostgresDsn:
        """Ensure database URL uses asyncpg driver."""
        if isinstance(v, str):
            if v.startswith("postgresql://"):
                v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
            return PostgresDsn(v)
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
