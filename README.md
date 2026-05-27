# Monster Quant

A-share emotion and capital-flow quant platform for main-theme, leader-stock,
second-wave, auction-above-expectation, hot-money, and risk-cycle research.

## Quick Start

```powershell
.\scripts\monster.cmd setup
.\scripts\monster.cmd cli -Provider mock
.\scripts\monster.cmd api -Provider akshare
```

Frontend:

```powershell
.\scripts\monster.cmd frontend
```

Open:

```text
http://127.0.0.1:5173
```

For the frontend to show data, keep the API running in another terminal:

```powershell
.\scripts\monster.cmd api -Provider mock
```

## What Is Included

- FastAPI backend
- PostgreSQL and Redis Docker Compose
- SQLAlchemy database models
- Collector adapter interfaces for akshare, pytdx, and tushare
- Theme ranking, emotion cycle, MonsterScore, TOP10 pool
- Risk engine and daily Markdown review
- Minimal Vue/ECharts frontend shell
- Legacy CSV backtest sandbox kept under `quant_trading`

## Backend

```powershell
pip install -e .[dev]
$env:DATA_PROVIDER = "akshare"
uvicorn monster_quant.api.app:create_app --factory --reload
```

Use `DATA_PROVIDER=mock` when you want a deterministic offline demo.

## CLI Review

```powershell
.\scripts\monster.cmd cli -Provider akshare
```

## Docker Services

```powershell
docker compose -f docker/docker-compose.yml up -d
```

Or:

```powershell
.\scripts\monster.cmd docker
```

## Push Helper

```powershell
.\scripts\push.cmd -Message "Update Monster Quant"
```

## Real Data

The default real-data adapter is `akshare`. It currently builds the phase-one
snapshot from public A-share endpoints and converts them into Monster Quant
signals:

- limit-up pool and emotion breadth
- concept/theme heat
- stock candidates with capital, emotion, pattern, chip, and auction fields
