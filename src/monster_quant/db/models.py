from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StockBasic(Base):
    __tablename__ = "stock_basic"

    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    industry: Mapped[str] = mapped_column(String(64), default="")
    market: Mapped[str] = mapped_column(String(16), default="")


class StockDaily(Base):
    __tablename__ = "stock_daily"
    __table_args__ = (UniqueConstraint("code", "trade_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(16), index=True)
    trade_date: Mapped[date] = mapped_column(Date, index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)
    turnover_rate: Mapped[float] = mapped_column(Float, default=0)


class LimitUpPool(Base):
    __tablename__ = "limit_up_pool"
    __table_args__ = (UniqueConstraint("code", "trade_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(16), index=True)
    name: Mapped[str] = mapped_column(String(64))
    trade_date: Mapped[date] = mapped_column(Date, index=True)
    theme: Mapped[str] = mapped_column(String(64), default="")
    consecutive_boards: Mapped[int] = mapped_column(Integer, default=1)
    sealed_amount: Mapped[float] = mapped_column(Float, default=0)
    failed: Mapped[int] = mapped_column(Integer, default=0)


class DragonTiger(Base):
    __tablename__ = "dragon_tiger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(16), index=True)
    name: Mapped[str] = mapped_column(String(64))
    trade_date: Mapped[date] = mapped_column(Date, index=True)
    seat_name: Mapped[str] = mapped_column(String(128))
    buy_amount: Mapped[float] = mapped_column(Float, default=0)
    sell_amount: Mapped[float] = mapped_column(Float, default=0)


class BlockTrade(Base):
    __tablename__ = "block_trade"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(16), index=True)
    name: Mapped[str] = mapped_column(String(64))
    trade_date: Mapped[date] = mapped_column(Date, index=True)
    discount_pct: Mapped[float] = mapped_column(Float, default=0)
    amount: Mapped[float] = mapped_column(Float, default=0)
    buyer: Mapped[str] = mapped_column(String(128), default="")


class EmotionCycleRecord(Base):
    __tablename__ = "emotion_cycle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trade_date: Mapped[date] = mapped_column(Date, unique=True, index=True)
    stage: Mapped[str] = mapped_column(String(32))
    limit_up_count: Mapped[int] = mapped_column(Integer)
    limit_down_count: Mapped[int] = mapped_column(Integer)
    failed_limit_up_rate: Mapped[float] = mapped_column(Float)
    max_board_height: Mapped[int] = mapped_column(Integer)


class MonsterScoreRecord(Base):
    __tablename__ = "monster_score"
    __table_args__ = (UniqueConstraint("code", "trade_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(16), index=True)
    name: Mapped[str] = mapped_column(String(64))
    theme: Mapped[str] = mapped_column(String(64), index=True)
    trade_date: Mapped[date] = mapped_column(Date, index=True)
    total: Mapped[float] = mapped_column(Float)
    capital: Mapped[float] = mapped_column(Float)
    emotion: Mapped[float] = mapped_column(Float)
    pattern: Mapped[float] = mapped_column(Float)
    chip: Mapped[float] = mapped_column(Float)
    reasons: Mapped[str] = mapped_column(Text, default="")
    risk_notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
