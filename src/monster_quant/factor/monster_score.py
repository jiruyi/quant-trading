from __future__ import annotations

from monster_quant.domain import MonsterScore, StockSignal, ThemeRank


def score_stock(stock: StockSignal, theme_ranks: list[ThemeRank]) -> MonsterScore:
    theme_lookup = {item.name: item.score for item in theme_ranks}
    theme_heat = theme_lookup.get(stock.theme, 0.0)

    capital = clamp(
        normalize(stock.main_net_inflow, 0, 3) * 45
        + stock.hot_money_score * 0.35
        + stock.block_trade_discount * 4
    )
    emotion = clamp(
        stock.limit_up_strength * 0.35
        + min(stock.consecutive_boards, 6) / 6 * 30
        + leader_score(stock.leader_rank)
        + theme_heat * 0.15
    )
    pattern = clamp(
        stock.second_wave_score * 0.5
        + stock.volume_ratio * 8
        + (15 if is_auction_above_expectation(stock) else 0)
    )
    chip = clamp(
        stock.chip_concentration * 0.55
        + normalize(35 - stock.turnover_rate, 0, 35) * 45
    )
    total = round(capital * 0.3 + emotion * 0.3 + pattern * 0.2 + chip * 0.2, 2)
    reasons = build_reasons(stock, theme_heat)
    risks = build_risks(stock)
    return MonsterScore(stock.code, stock.name, stock.theme, total, round(capital, 2), round(emotion, 2), round(pattern, 2), round(chip, 2), reasons, risks)


def top_monsters(stocks: list[StockSignal], theme_ranks: list[ThemeRank], limit: int = 10) -> list[MonsterScore]:
    scored = [score_stock(stock, theme_ranks) for stock in stocks]
    return sorted(scored, key=lambda item: item.total, reverse=True)[:limit]


def is_auction_above_expectation(stock: StockSignal) -> bool:
    return (
        2 <= stock.auction_gap_pct <= 6
        and stock.auction_volume_ratio > 3
        and stock.yesterday_limit_up
    )


def leader_score(rank: int) -> float:
    if rank <= 1:
        return 25.0
    if rank == 2:
        return 18.0
    if rank <= 4:
        return 10.0
    return 3.0


def normalize(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.0
    return clamp((value - low) / (high - low), 0.0, 1.0)


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def build_reasons(stock: StockSignal, theme_heat: float) -> list[str]:
    reasons: list[str] = []
    if theme_heat >= 75:
        reasons.append("主线热度靠前")
    if stock.leader_rank <= 2:
        reasons.append("龙头/前排辨识度")
    if stock.second_wave_score >= 80:
        reasons.append("二波结构较强")
    if is_auction_above_expectation(stock):
        reasons.append("竞价超预期")
    if stock.hot_money_score >= 80:
        reasons.append("游资接力活跃")
    return reasons or ["综合强度一般，作为观察样本"]


def build_risks(stock: StockSignal) -> list[str]:
    risks: list[str] = []
    if stock.turnover_rate > 25:
        risks.append("换手偏高")
    if stock.main_net_inflow < 0:
        risks.append("主力净流出")
    if stock.leader_rank > 4:
        risks.append("辨识度偏后排")
    return risks
