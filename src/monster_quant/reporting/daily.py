from __future__ import annotations

from monster_quant.domain import EmotionStage, MonsterScore, ThemeRank


def build_daily_review(
    stage: EmotionStage,
    position_limit: float,
    themes: list[ThemeRank],
    monsters: list[MonsterScore],
) -> str:
    lines = [
        "# Monster Quant Daily Review",
        "",
        f"- Emotion cycle: {stage.value}",
        f"- Suggested max position: {position_limit:.0%}",
        "",
        "## Main Themes",
    ]
    for index, theme in enumerate(themes[:5], start=1):
        lines.append(f"{index}. {theme.name} - {theme.score:.2f}")

    lines.extend(["", "## TOP Monsters"])
    for index, monster in enumerate(monsters, start=1):
        reason = "、".join(monster.reasons)
        risk = "、".join(monster.risk_notes) if monster.risk_notes else "无明显模型风险"
        lines.append(f"{index}. {monster.code} {monster.name} [{monster.theme}] {monster.total:.2f} - {reason}；风险：{risk}")

    lines.extend(["", "## Next Day Focus", "- 只跟踪主线前排。", "- 情绪退潮时降低仓位。", "- 优先观察竞价超预期、龙头低吸、二波启动。"])
    return "\n".join(lines)
