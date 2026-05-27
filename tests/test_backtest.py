from pathlib import Path

from quant_trading.backtest import run_long_only_backtest
from quant_trading.data import load_price_csv
from quant_trading.metrics import max_drawdown, total_return
from quant_trading.strategy import MovingAverageCross


def test_moving_average_backtest_runs_on_sample_data() -> None:
    bars = load_price_csv(Path("data/sample_prices.csv"))
    signals = MovingAverageCross(short_window=3, long_window=5).generate(bars)

    result = run_long_only_backtest(bars, signals, initial_cash=10_000)

    assert len(result.equity_curve) == len(bars)
    assert result.final_equity > 0
    assert result.trades >= 1


def test_metrics_are_bounded_for_sample_data() -> None:
    bars = load_price_csv(Path("data/sample_prices.csv"))
    signals = MovingAverageCross(short_window=3, long_window=5).generate(bars)
    result = run_long_only_backtest(bars, signals, initial_cash=10_000)

    assert total_return(result.equity_curve) > -1
    assert max_drawdown(result.equity_curve) <= 0
