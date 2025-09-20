"""Application settings leveraging pydantic for validation."""
from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, HttpUrl, AnyUrl


class Settings(BaseSettings):
    environment: str = Field("development", env="ENVIRONMENT")
    version: str = "0.1.0"
    api_v1_prefix: str = "/api"

    secret_key: str = Field("change-me", env="SECRET_KEY")
    jwt_algorithm: str = "HS256"
    jwt_access_expire_minutes: int = Field(30, env="JWT_EXPIRE_MIN")
    jwt_refresh_expire_minutes: int = 60 * 24

    database_url: AnyUrl = Field("postgresql+asyncpg://postgres:postgres@db:5432/money_trader", env="DATABASE_URL")
    redis_url: AnyUrl = Field("redis://redis:6379/0", env="REDIS_URL")

    dev_mode: bool = Field(True, env="DEV_MODE")
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])

    rate_limit_default: int = Field(60, env="RATE_LIMIT_DEFAULT")
    rate_limit_window_seconds: int = Field(60, env="RATE_LIMIT_WINDOW")

    binance_ws_url: str | None = Field(None, env="BINANCE_WS_URL")
    alphavantage_key: str | None = Field(None, env="ALPHAVANTAGE_KEY")
    polygon_key: str | None = Field(None, env="POLYGON_KEY")

    smtp_host: str = Field("mailhog", env="SMTP_HOST")
    smtp_port: int = Field(1025, env="SMTP_PORT")

    price_symbols_crypto: List[str] = Field(
        default_factory=lambda: ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    )
    price_symbols_forex: List[str] = Field(
        default_factory=lambda: ["EURUSD", "GBPUSD", "USDJPY"],
    )

    max_free_alerts: int = Field(3, env="MAX_FREE_ALERTS")
    max_free_signals_per_day: int = Field(3, env="MAX_FREE_SIGNALS")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
