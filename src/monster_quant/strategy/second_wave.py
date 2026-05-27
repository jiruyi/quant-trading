from __future__ import annotations

from monster_quant.domain import StockSignal


def select_second_wave_candidates(stocks: list[StockSignal]) -> list[StockSignal]:
    return [
        stock
        for stock in stocks
        if stock.second_wave_score >= 80
        and stock.volume_ratio >= 2
        and stock.main_net_inflow > 0
    ]
