from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from quant_trading.models import Bar, EquityPoint, Signal


@dataclass(frozen=True)
class BacktestResult:
    equity_curve: list[EquityPoint]
    trades: int

    @property
    def final_equity(self) -> float:
        return self.equity_curve[-1].equity


def run_long_only_backtest(
    bars: Sequence[Bar],
    signals: Sequence[Signal],
    initial_cash: float = 100_000.0,
) -> BacktestResult:
    if len(bars) != len(signals):
        raise ValueError("bars and signals must have the same length")
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")

    cash = initial_cash
    shares = 0
    trades = 0
    curve: list[EquityPoint] = []

    for bar, signal in zip(bars, signals, strict=True):
        if signal.target_position not in (0, 1):
            raise ValueError("long-only target_position must be 0 or 1")

        if signal.target_position == 1 and shares == 0:
            shares = int(cash // bar.close)
            cash -= shares * bar.close
            trades += int(shares > 0)
        elif signal.target_position == 0 and shares > 0:
            cash += shares * bar.close
            shares = 0
            trades += 1

        equity = cash + shares * bar.close
        curve.append(EquityPoint(bar.date, equity, shares, cash, bar.close))

    return BacktestResult(equity_curve=curve, trades=trades)
