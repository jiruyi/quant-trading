from __future__ import annotations

from monster_quant.domain import EmotionStage, MonsterScore
from monster_quant.emotion import position_limit


def single_stock_limit(score: MonsterScore, stage: EmotionStage) -> float:
    if stage is EmotionStage.EBB:
        return 0.0
    if score.total >= 85:
        return 0.2
    if score.total >= 75:
        return 0.15
    return 0.08


def risk_level(stage: EmotionStage, failed_limit_up_rate: float) -> str:
    if stage is EmotionStage.EBB or failed_limit_up_rate > 0.4:
        return "high"
    if stage in {EmotionStage.CLIMAX, EmotionStage.ICE}:
        return "medium"
    return "low"


def portfolio_limit(stage: EmotionStage) -> float:
    return position_limit(stage)
