from __future__ import annotations

import argparse
from pathlib import Path

from quant_trading.backtest import run_long_only_backtest
from quant_trading.data import load_price_csv
from quant_trading.metrics import max_drawdown, sharpe_ratio, total_return
from quant_trading.strategy import MovingAverageCross


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a simple moving-average backtest.")
    parser.add_argument("--prices", type=Path, required=True)
    parser.add_argument("--short-window", type=int, default=5)
    parser.add_argument("--long-window", type=int, default=20)
    parser.add_argument("--initial-cash", type=float, default=100_000.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    bars = load_price_csv(args.prices)
    strategy = MovingAverageCross(args.short_window, args.long_window)
    result = run_long_only_backtest(
        bars,
        strategy.generate(bars),
        initial_cash=args.initial_cash,
    )

    print(f"bars: {len(bars)}")
    print(f"trades: {result.trades}")
    print(f"final_equity: {result.final_equity:.2f}")
    print(f"total_return: {total_return(result.equity_curve):.2%}")
    print(f"max_drawdown: {max_drawdown(result.equity_curve):.2%}")
    print(f"sharpe: {sharpe_ratio(result.equity_curve):.2f}")
    return 0
