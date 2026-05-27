from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from monster_quant.crawler.base import MarketDataProvider
from monster_quant.domain import MarketSnapshot, StockSignal, ThemeSignal


class AkshareProvider(MarketDataProvider):
    def snapshot(self, trade_date: date | None = None) -> MarketSnapshot:
        ak = import_akshare()
        current_date, limit_pool, strong_pool = load_limit_pool(ak, trade_date)
        concept_rank = safe_call(lambda: ak.stock_board_concept_name_em())
        capital_flow = safe_call(lambda: ak.stock_individual_fund_flow_rank(indicator="今日"))

        themes = build_theme_signals(concept_rank)
        stocks = build_stock_signals(limit_pool, strong_pool, capital_flow, themes)
        limit_up_count = frame_len(limit_pool)
        failed_limit_up_rate = estimate_failed_rate(strong_pool)
        max_height = estimate_max_height(limit_pool)

        return MarketSnapshot(
            trade_date=current_date,
            limit_up_count=limit_up_count,
            limit_down_count=0,
            failed_limit_up_rate=failed_limit_up_rate,
            max_board_height=max_height,
            twenty_cm_count=estimate_twenty_cm_count(limit_pool),
            theme_signals=themes,
            stock_signals=stocks,
        )

    def collect_all(self, trade_date: date | None = None) -> MarketSnapshot:
        return self.snapshot(trade_date)


def import_akshare() -> Any:
    try:
        import akshare as ak
    except ImportError as exc:
        raise RuntimeError("akshare is not installed. Run: pip install -e .") from exc
    return ak


def safe_call(fn: Any) -> Any | None:
    try:
        return fn()
    except Exception:
        return None


def load_limit_pool(ak: Any, trade_date: date | None) -> tuple[date, Any | None, Any | None]:
    dates = [trade_date] if trade_date else [date.today() - timedelta(days=offset) for offset in range(31)]
    for current_date in dates:
        if current_date is None:
            continue
        day = current_date.strftime("%Y%m%d")
        limit_pool = safe_call(lambda: ak.stock_zt_pool_em(date=day))
        strong_pool = safe_call(lambda: ak.stock_zt_pool_strong_em(date=day))
        if frame_len(limit_pool) > 0:
            return current_date, limit_pool, strong_pool
    fallback_date = trade_date or date.today()
    return fallback_date, None, None


def frame_len(frame: Any | None) -> int:
    if frame is None:
        return 0
    return int(getattr(frame, "shape", [0])[0])


def col(row: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if name in row and row[name] == row[name]:
            return row[name]
    return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).replace("%", "").replace(",", "").strip()
        if text in {"", "-", "None", "nan"}:
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def build_theme_signals(concept_rank: Any | None) -> list[ThemeSignal]:
    if concept_rank is None or frame_len(concept_rank) == 0:
        return []

    themes: list[ThemeSignal] = []
    for index, row in concept_rank.head(20).iterrows():
        name = str(col(row, "板块名称", "概念名称", "名称", default=f"theme-{index}"))
        pct = as_float(col(row, "涨跌幅", "涨跌幅%", default=0))
        net_inflow = as_float(col(row, "净流入", "主力净流入", default=0))
        stock_count = int(max(as_float(col(row, "上涨家数", "涨停家数", default=max(pct, 0))), 0))
        themes.append(
            ThemeSignal(
                name=name,
                limit_up_count=stock_count,
                net_inflow=normalize_money(net_inflow),
                continuity_days=1 + int(max(pct, 0) // 2),
                height=min(6, max(1, int(max(pct, 0) // 2) + 1)),
                news_heat=min(100, max(0, pct * 10 + stock_count)),
            )
        )
    return themes


def build_stock_signals(
    limit_pool: Any | None,
    strong_pool: Any | None,
    capital_flow: Any | None,
    themes: list[ThemeSignal],
) -> list[StockSignal]:
    if limit_pool is None or frame_len(limit_pool) == 0:
        return []

    theme_name = themes[0].name if themes else "未知主线"
    flow_by_code = index_capital_flow(capital_flow)
    stocks: list[StockSignal] = []
    for rank, (_, row) in enumerate(limit_pool.head(80).iterrows(), start=1):
        code = normalize_code(col(row, "代码", "股票代码", default=""))
        name = str(col(row, "名称", "股票简称", default=code))
        close = as_float(col(row, "最新价", "收盘价", default=0))
        turnover = as_float(col(row, "换手率", default=0))
        amount = as_float(col(row, "成交额", default=0))
        boards = int(max(as_float(col(row, "连板数", "几天几板", default=1)), 1))
        sealed = as_float(col(row, "封单资金", "封板资金", default=0))
        flow = flow_by_code.get(code, {})
        main_inflow = normalize_money(flow.get("main_net_inflow", amount * 0.03))
        stock_theme = str(col(row, "所属行业", "板块", default=theme_name)) or theme_name

        stocks.append(
            StockSignal(
                code=code,
                name=name,
                theme=stock_theme,
                close=close,
                market_cap=as_float(col(row, "流通市值", "总市值", default=0)),
                main_net_inflow=main_inflow,
                hot_money_score=min(100, 45 + boards * 10 + min(rank, 10)),
                block_trade_discount=0,
                limit_up_strength=min(100, 60 + boards * 8 + normalize_money(sealed) * 2),
                consecutive_boards=boards,
                leader_rank=rank,
                turnover_rate=turnover,
                volume_ratio=max(1, normalize_money(amount) / 2),
                second_wave_score=min(100, 45 + boards * 7 + max(0, 20 - turnover)),
                chip_concentration=max(0, min(100, 80 - turnover)),
                yesterday_limit_up=boards >= 2,
                auction_gap_pct=as_float(col(row, "涨跌幅", default=0)),
                auction_volume_ratio=max(1, normalize_money(amount) / 3),
            )
        )
    return stocks


def index_capital_flow(capital_flow: Any | None) -> dict[str, dict[str, float]]:
    if capital_flow is None or frame_len(capital_flow) == 0:
        return {}
    result: dict[str, dict[str, float]] = {}
    for _, row in capital_flow.iterrows():
        code = normalize_code(col(row, "代码", "股票代码", default=""))
        result[code] = {
            "main_net_inflow": as_float(col(row, "主力净流入-净额", "今日主力净流入-净额", "主力净流入", default=0))
        }
    return result


def normalize_code(value: Any) -> str:
    text = str(value).strip()
    return text.zfill(6) if text.isdigit() else text


def normalize_money(value: float) -> float:
    value = abs(as_float(value))
    if value >= 100_000_000:
        return value / 100_000_000
    if value >= 10_000:
        return value / 10_000
    return value


def estimate_failed_rate(strong_pool: Any | None) -> float:
    if strong_pool is None or frame_len(strong_pool) == 0:
        return 0.0
    failed = 0
    total = frame_len(strong_pool)
    for _, row in strong_pool.iterrows():
        failed += int(as_float(col(row, "炸板次数", default=0)) > 0)
    return round(failed / total, 4) if total else 0.0


def estimate_max_height(limit_pool: Any | None) -> int:
    if limit_pool is None or frame_len(limit_pool) == 0:
        return 0
    heights = [int(max(as_float(col(row, "连板数", "几天几板", default=1)), 1)) for _, row in limit_pool.iterrows()]
    return max(heights) if heights else 0


def estimate_twenty_cm_count(limit_pool: Any | None) -> int:
    if limit_pool is None or frame_len(limit_pool) == 0:
        return 0
    count = 0
    for _, row in limit_pool.iterrows():
        pct = as_float(col(row, "涨跌幅", default=0))
        count += int(pct >= 19)
    return count
