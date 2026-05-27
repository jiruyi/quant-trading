from __future__ import annotations

from math import sqrt

from quant_trading.models import EquityPoint


def total_return(curve: list[EquityPoint]) -> float:
    if len(curve) < 2:
        return 0.0
    return curve[-1].equity / curve[0].equity - 1.0


def max_drawdown(curve: list[EquityPoint]) -> float:
    peak = curve[0].equity
    worst = 0.0
    for point in curve:
        peak = max(peak, point.equity)
        drawdown = point.equity / peak - 1.0
        worst = min(worst, drawdown)
    return worst


def sharpe_ratio(curve: list[EquityPoint], periods_per_year: int = 252) -> float:
    returns = [
        curve[index].equity / curve[index - 1].equity - 1.0
        for index in range(1, len(curve))
    ]
    if len(returns) < 2:
        return 0.0
    avg = sum(returns) / len(returns)
    variance = sum((item - avg) ** 2 for item in returns) / (len(returns) - 1)
    if variance == 0:
        return 0.0
    return avg / sqrt(variance) * sqrt(periods_per_year)
