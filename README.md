# Quant Trading

A small Python quant-trading playground with a moving-average crossover strategy,
a deterministic CSV backtest engine, and tests.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
python -m quant_trading --prices data/sample_prices.csv --short-window 5 --long-window 20
python -m pytest
```

## What Is Included

- CSV price loading with typed bars
- Moving-average crossover signal generation
- Long-only backtest engine
- Return, drawdown, and Sharpe metrics
- CLI entry point and sample data

