from __future__ import annotations

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from monster_quant.config import get_settings
from monster_quant.db.models import Base


def get_engine() -> Engine:
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def get_session_factory(engine: Engine | None = None) -> sessionmaker:
    return sessionmaker(bind=engine or get_engine(), autoflush=False, autocommit=False)


def init_db(engine: Engine | None = None) -> None:
    Base.metadata.create_all(bind=engine or get_engine())
