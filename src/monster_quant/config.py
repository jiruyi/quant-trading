from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Monster Quant"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://monster:monster@localhost:5432/monster_quant",
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    data_provider: str = os.getenv("DATA_PROVIDER", "akshare")


def get_settings() -> Settings:
    return Settings()
