from __future__ import annotations

from monster_quant.domain import EmotionStage, MarketSnapshot


def classify_emotion(snapshot: MarketSnapshot) -> EmotionStage:
    if snapshot.failed_limit_up_rate > 0.4 or snapshot.limit_down_count >= 20:
        return EmotionStage.EBB
    if snapshot.limit_up_count <= 30 and snapshot.max_board_height <= 3:
        return EmotionStage.ICE
    if snapshot.limit_up_count >= 90 and snapshot.failed_limit_up_rate < 0.2:
        return EmotionStage.CLIMAX
    if snapshot.limit_up_count >= 60 and snapshot.max_board_height >= 5:
        return EmotionStage.MAIN_RISE
    return EmotionStage.REPAIR


def position_limit(stage: EmotionStage) -> float:
    return {
        EmotionStage.ICE: 0.3,
        EmotionStage.REPAIR: 0.5,
        EmotionStage.MAIN_RISE: 0.7,
        EmotionStage.CLIMAX: 0.4,
        EmotionStage.EBB: 0.1,
    }[stage]
