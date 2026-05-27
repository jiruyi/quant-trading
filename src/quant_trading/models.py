from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Bar:
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class Signal:
    date: date
    target_position: int
    reason: str


@dataclass(frozen=True)
class EquityPoint:
    date: date
    equity: float
    position: int
    cash: float
    close: float
