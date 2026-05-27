from __future__ import annotations

from dataclasses import asdict

from monster_quant.crawler import get_provider
from monster_quant.emotion import classify_emotion
from monster_quant.factor import rank_themes, top_monsters
from monster_quant.risk import portfolio_limit, risk_level
from monster_quant.strategy import (
    select_auction_candidates,
    select_leader_pullback_candidates,
    select_second_wave_candidates,
)


def market_dashboard() -> dict[str, object]:
    snapshot = get_provider().snapshot()
    stage = classify_emotion(snapshot)
    themes = rank_themes(snapshot.theme_signals)
    monsters = top_monsters(snapshot.stock_signals, themes)
    return {
        "trade_date": snapshot.trade_date.isoformat(),
        "emotion": {
            "stage": stage.value,
            "risk_level": risk_level(stage, snapshot.failed_limit_up_rate),
            "portfolio_limit": portfolio_limit(stage),
        },
        "themes": [asdict(item) for item in themes],
        "monsters": [asdict(item) for item in monsters],
        "strategies": {
            "auction_above_expectation": [asdict(item) for item in select_auction_candidates(snapshot.stock_signals)],
            "leader_pullback": [asdict(item) for item in select_leader_pullback_candidates(snapshot.stock_signals)],
            "second_wave": [asdict(item) for item in select_second_wave_candidates(snapshot.stock_signals)],
        },
    }
