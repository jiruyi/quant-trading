from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from monster_quant.scheduler.jobs import collect_market_data, generate_daily_review


def build_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(collect_market_data, "cron", hour=15, minute=10, id="collect_market_data")
    scheduler.add_job(generate_daily_review, "cron", hour=16, minute=0, id="generate_daily_review")
    return scheduler
