from __future__ import annotations

from monster_quant.domain import StockSignal
from monster_quant.factor import is_auction_above_expectation


def select_auction_candidates(stocks: list[StockSignal]) -> list[StockSignal]:
    return [stock for stock in stocks if is_auction_above_expectation(stock)]
