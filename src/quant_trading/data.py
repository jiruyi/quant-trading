from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from quant_trading.models import Bar


def load_price_csv(path: str | Path) -> list[Bar]:
    bars: list[Bar] = []
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"date", "open", "high", "low", "close", "volume"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(f"missing CSV columns: {missing_text}")

        for row in reader:
            bars.append(
                Bar(
                    date=date.fromisoformat(row["date"]),
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row["volume"]),
                )
            )

    if not bars:
        raise ValueError("price CSV is empty")
    return bars
