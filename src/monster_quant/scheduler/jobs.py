from __future__ import annotations

from datetime import date

from monster_quant.crawler import get_provider
from monster_quant.emotion import classify_emotion
from monster_quant.factor import rank_themes, top_monsters
from monster_quant.reporting import build_daily_review
from monster_quant.risk import portfolio_limit


def collect_market_data(trade_date: date | None = None) -> dict[str, object]:
    snapshot = get_provider().collect_all(trade_date)
    return {"trade_date": snapshot.trade_date.isoformat(), "stock_count": len(snapshot.stock_signals)}


def generate_daily_review() -> str:
    snapshot = get_provider().snapshot()
    stage = classify_emotion(snapshot)
    themes = rank_themes(snapshot.theme_signals)
    monsters = top_monsters(snapshot.stock_signals, themes)
    return build_daily_review(stage, portfolio_limit(stage), themes, monsters)
