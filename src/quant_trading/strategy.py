from __future__ import annotations

from collections.abc import Sequence

from quant_trading.models import Bar, Signal


class MovingAverageCross:
    def __init__(self, short_window: int = 10, long_window: int = 30) -> None:
        if short_window <= 0 or long_window <= 0:
            raise ValueError("windows must be positive")
        if short_window >= long_window:
            raise ValueError("short_window must be smaller than long_window")
        self.short_window = short_window
        self.long_window = long_window

    def generate(self, bars: Sequence[Bar]) -> list[Signal]:
        closes = [bar.close for bar in bars]
        signals: list[Signal] = []
        current_position = 0

        for index, bar in enumerate(bars):
            if index + 1 < self.long_window:
                signals.append(Signal(bar.date, current_position, "warming_up"))
                continue

            short_ma = mean(closes[index + 1 - self.short_window : index + 1])
            long_ma = mean(closes[index + 1 - self.long_window : index + 1])
            target = 1 if short_ma > long_ma else 0

            if target != current_position:
                reason = "bullish_cross" if target == 1 else "bearish_cross"
                current_position = target
            else:
                reason = "hold"

            signals.append(Signal(bar.date, current_position, reason))

        return signals


def mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)
