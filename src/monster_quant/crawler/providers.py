from __future__ import annotations

from datetime import date

from monster_quant.config import get_settings
from monster_quant.crawler.akshare_provider import AkshareProvider
from monster_quant.crawler.base import MarketDataProvider
from monster_quant.crawler.mock import load_mock_snapshot
from monster_quant.domain import MarketSnapshot


class MockProvider(MarketDataProvider):
    def snapshot(self, trade_date: date | None = None) -> MarketSnapshot:
        return load_mock_snapshot(trade_date)

    def collect_all(self, trade_date: date | None = None) -> MarketSnapshot:
        return self.snapshot(trade_date)


class ExternalProviderPlaceholder(MarketDataProvider):
    def __init__(self, name: str) -> None:
        self.name = name

    def snapshot(self, trade_date: date | None = None) -> MarketSnapshot:
        raise NotImplementedError(f"{self.name} adapter is not configured yet")

    def collect_all(self, trade_date: date | None = None) -> MarketSnapshot:
        return self.snapshot(trade_date)


def get_provider() -> MarketDataProvider:
    provider = get_settings().data_provider.lower()
    if provider == "mock":
        return MockProvider()
    if provider == "akshare":
        return AkshareProvider()
    if provider in {"pytdx", "tushare"}:
        return ExternalProviderPlaceholder(provider)
    raise ValueError(f"unsupported DATA_PROVIDER: {provider}")
