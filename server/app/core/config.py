"""Environment-driven application configuration."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings consumed by Foundation.

    DATABASE_URL is the sole database endpoint contract. In production it is
    expected to point at the Cloudflare Hyperdrive endpoint; local development
    may point directly at Neon or a local PostgreSQL instance.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "GDG Flutter Workshop Backend"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: SecretStr = Field(validation_alias="DATABASE_URL")
    database_connect_timeout_seconds: int = Field(default=10, ge=1, le=120)
    database_pool_size: int = Field(default=5, ge=1, le=50)
    database_max_overflow: int = Field(default=10, ge=0, le=100)
    jwt_secret_key: SecretStr = Field(validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_access_token_minutes: int = Field(
        default=60, ge=1, le=1440, validation_alias="JWT_ACCESS_TOKEN_MINUTES"
    )
    google_oauth_client_id: str | None = Field(
        default=None, validation_alias="GOOGLE_OAUTH_CLIENT_ID"
    )

    @property
    def database_dsn(self) -> str:
        """Return the connection string only to database infrastructure code."""
        return self.database_url.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """Load and validate settings once per process; fail clearly if required values are absent."""
    return Settings()
