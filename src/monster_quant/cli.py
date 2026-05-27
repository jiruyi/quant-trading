from __future__ import annotations

from monster_quant.crawler import get_provider
from monster_quant.emotion import classify_emotion, position_limit
from monster_quant.factor import rank_themes, top_monsters
from monster_quant.reporting import build_daily_review


def main() -> int:
    snapshot = get_provider().snapshot()
    stage = classify_emotion(snapshot)
    themes = rank_themes(snapshot.theme_signals)
    monsters = top_monsters(snapshot.stock_signals, themes)
    print(build_daily_review(stage, position_limit(stage), themes, monsters))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
