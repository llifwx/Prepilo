from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

JWT_ALGORITHM = "HS256"
_WEAK_SECRET = "change-me-in-production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = Field(default="local", alias="APP_ENV")
    database_url: str = Field(default="sqlite:///./prepilo.db", alias="DATABASE_URL")
    secret_key: str = Field(alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(
        default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    allowed_origins: str = Field(
        default="http://localhost:3000", alias="ALLOWED_ORIGINS"
    )

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_be_strong(cls, v: str) -> str:
        if v == _WEAK_SECRET or len(v) < 32:
            raise ValueError(
                "SECRET_KEY must be set to a strong random value (min 32 chars)"
            )
        return v

    @field_validator("database_url")
    @classmethod
    def no_sqlite_in_production(cls, v: str, info) -> str:
        env = (info.data or {}).get("app_env", "local")
        if env != "local" and v.startswith("sqlite"):
            raise ValueError("SQLite cannot be used in non-local environments")
        return v

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
