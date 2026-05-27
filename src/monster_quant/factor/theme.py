from __future__ import annotations

from monster_quant.domain import ThemeRank, ThemeSignal


def rank_themes(signals: list[ThemeSignal]) -> list[ThemeRank]:
    ranks = [
        ThemeRank(name=signal.name, score=theme_score(signal), signal=signal)
        for signal in signals
    ]
    return sorted(ranks, key=lambda item: item.score, reverse=True)


def theme_score(signal: ThemeSignal) -> float:
    raw = (
        signal.limit_up_count * 3.0
        + signal.net_inflow * 4.0
        + signal.continuity_days * 6.0
        + signal.height * 5.0
        + signal.news_heat * 0.15
    )
    return round(min(raw, 100.0), 2)
