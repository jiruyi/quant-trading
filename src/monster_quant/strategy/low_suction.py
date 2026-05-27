from __future__ import annotations

from monster_quant.domain import StockSignal


def select_leader_pullback_candidates(stocks: list[StockSignal]) -> list[StockSignal]:
    return [
        stock
        for stock in stocks
        if stock.leader_rank <= 2
        and stock.volume_ratio < 4
        and stock.main_net_inflow > 0
        and stock.turnover_rate < 25
    ]
