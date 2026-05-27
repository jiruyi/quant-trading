from __future__ import annotations

from fastapi import FastAPI

from monster_quant.crawler.mock import load_mock_snapshot
from monster_quant.emotion import classify_emotion, position_limit
from monster_quant.factor import rank_themes, top_monsters
from monster_quant.reporting import build_daily_review


def create_app() -> FastAPI:
    app = FastAPI(title="Monster Quant", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/market/emotion")
    def market_emotion() -> dict[str, object]:
        snapshot = load_mock_snapshot()
        stage = classify_emotion(snapshot)
        return {
            "trade_date": snapshot.trade_date.isoformat(),
            "stage": stage.value,
            "position_limit": position_limit(stage),
            "limit_up_count": snapshot.limit_up_count,
            "limit_down_count": snapshot.limit_down_count,
            "failed_limit_up_rate": snapshot.failed_limit_up_rate,
            "max_board_height": snapshot.max_board_height,
        }

    @app.get("/themes/top")
    def themes_top() -> list[dict[str, object]]:
        snapshot = load_mock_snapshot()
        return [
            {
                "name": item.name,
                "score": item.score,
                "limit_up_count": item.signal.limit_up_count,
                "net_inflow": item.signal.net_inflow,
                "continuity_days": item.signal.continuity_days,
                "height": item.signal.height,
            }
            for item in rank_themes(snapshot.theme_signals)
        ]

    @app.get("/monster/top")
    def monster_top(limit: int = 10) -> list[dict[str, object]]:
        snapshot = load_mock_snapshot()
        themes = rank_themes(snapshot.theme_signals)
        return [monster.__dict__ for monster in top_monsters(snapshot.stock_signals, themes, limit=limit)]

    @app.get("/review/daily", response_model=str)
    def daily_review() -> str:
        snapshot = load_mock_snapshot()
        stage = classify_emotion(snapshot)
        themes = rank_themes(snapshot.theme_signals)
        monsters = top_monsters(snapshot.stock_signals, themes)
        return build_daily_review(stage, position_limit(stage), themes, monsters)

    return app


app = create_app()
