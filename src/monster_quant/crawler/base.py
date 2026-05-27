from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from monster_quant.domain import MarketSnapshot


class MarketDataProvider(ABC):
    @abstractmethod
    def snapshot(self, trade_date: date | None = None) -> MarketSnapshot:
        raise NotImplementedError

    @abstractmethod
    def collect_all(self, trade_date: date | None = None) -> MarketSnapshot:
        raise NotImplementedError
