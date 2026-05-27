from __future__ import annotations

from datetime import date

from monster_quant.domain import MarketSnapshot, StockSignal, ThemeSignal


def load_mock_snapshot(trade_date: date | None = None) -> MarketSnapshot:
    current_date = trade_date or date.today()
    themes = [
        ThemeSignal("机器人", limit_up_count=18, net_inflow=8.6, continuity_days=4, height=6, news_heat=86),
        ThemeSignal("AI", limit_up_count=13, net_inflow=6.2, continuity_days=3, height=4, news_heat=78),
        ThemeSignal("PCB", limit_up_count=9, net_inflow=3.7, continuity_days=2, height=3, news_heat=64),
    ]
    stocks = [
        StockSignal("000001", "主线机器人A", "机器人", 18.5, 8.8e9, 2.4, 92, 4.5, 96, 5, 1, 18, 3.8, 91, 84, True, 4.2, 4.8),
        StockSignal("000002", "机器人二波B", "机器人", 26.2, 1.2e10, 1.6, 84, 2.8, 88, 3, 2, 14, 2.9, 94, 77, True, 3.5, 3.6),
        StockSignal("000003", "AI中军C", "AI", 41.8, 8.6e10, 3.1, 72, 0.8, 72, 1, 2, 6, 1.8, 61, 69, False, 1.5, 2.2),
        StockSignal("000004", "PCB补涨D", "PCB", 13.4, 7.1e9, 0.7, 56, 1.2, 64, 2, 4, 22, 2.4, 58, 53, True, 2.8, 2.6),
        StockSignal("000005", "存储跟风E", "存储", 9.7, 6.5e9, -0.3, 32, 0.0, 45, 1, 6, 31, 1.1, 35, 42, False, -0.8, 0.9),
    ]
    return MarketSnapshot(
        trade_date=current_date,
        limit_up_count=74,
        limit_down_count=7,
        failed_limit_up_rate=0.22,
        max_board_height=6,
        twenty_cm_count=11,
        theme_signals=themes,
        stock_signals=stocks,
    )
