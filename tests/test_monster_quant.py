from monster_quant.crawler.mock import load_mock_snapshot
from monster_quant.crawler.akshare_provider import normalize_code, normalize_money
from monster_quant.emotion import EmotionStage, classify_emotion
from monster_quant.factor import is_auction_above_expectation, rank_themes, top_monsters
from monster_quant.reporting import build_daily_review


def test_phase_one_pipeline_outputs_top_monsters() -> None:
    snapshot = load_mock_snapshot()
    themes = rank_themes(snapshot.theme_signals)
    monsters = top_monsters(snapshot.stock_signals, themes, limit=3)

    assert themes[0].name == "机器人"
    assert len(monsters) == 3
    assert monsters[0].total >= monsters[-1].total
    assert "主线" in "、".join(monsters[0].reasons)


def test_emotion_cycle_and_review_are_generated() -> None:
    snapshot = load_mock_snapshot()
    stage = classify_emotion(snapshot)
    themes = rank_themes(snapshot.theme_signals)
    monsters = top_monsters(snapshot.stock_signals, themes)
    review = build_daily_review(stage, 0.7, themes, monsters)

    assert stage is EmotionStage.MAIN_RISE
    assert "Monster Quant Daily Review" in review
    assert "TOP Monsters" in review


def test_auction_above_expectation_rule() -> None:
    stock = load_mock_snapshot().stock_signals[0]

    assert is_auction_above_expectation(stock)


def test_akshare_helpers_normalize_values() -> None:
    assert normalize_code("1") == "000001"
    assert normalize_money(250_000_000) == 2.5
