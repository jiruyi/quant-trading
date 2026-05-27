from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum


class EmotionStage(StrEnum):
    ICE = "ice"
    REPAIR = "repair"
    MAIN_RISE = "main_rise"
    CLIMAX = "climax"
    EBB = "ebb"


@dataclass(frozen=True)
class ThemeSignal:
    name: str
    limit_up_count: int
    net_inflow: float
    continuity_days: int
    height: int
    news_heat: float = 0.0


@dataclass(frozen=True)
class StockSignal:
    code: str
    name: str
    theme: str
    close: float
    market_cap: float
    main_net_inflow: float
    hot_money_score: float
    block_trade_discount: float
    limit_up_strength: float
    consecutive_boards: int
    leader_rank: int
    turnover_rate: float
    volume_ratio: float
    second_wave_score: float
    chip_concentration: float
    yesterday_limit_up: bool
    auction_gap_pct: float = 0.0
    auction_volume_ratio: float = 0.0


@dataclass(frozen=True)
class MarketSnapshot:
    trade_date: date
    limit_up_count: int
    limit_down_count: int
    failed_limit_up_rate: float
    max_board_height: int
    twenty_cm_count: int
    theme_signals: list[ThemeSignal]
    stock_signals: list[StockSignal]


@dataclass(frozen=True)
class ThemeRank:
    name: str
    score: float
    signal: ThemeSignal


@dataclass(frozen=True)
class MonsterScore:
    code: str
    name: str
    theme: str
    total: float
    capital: float
    emotion: float
    pattern: float
    chip: float
    reasons: list[str]
    risk_notes: list[str]
