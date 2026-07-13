import json
from pathlib import Path


STATE_FILE = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\DayZServer"
    r"\profiles_ai_companion\DayZAICompanion\companion_state.json"
)

EXPECTED_COMPANION_ID = "burak_companion_001"


def get_health_status(health):
    if health <= 0:
        return "dead"

    if health < 25:
        return "critical"

    if health < 50:
        return "badly injured"

    if health < 75:
        return "injured"

    return "healthy"


def load_companion_state():
    if not STATE_FILE.exists():
        return None

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            state = json.load(file)

        if state.get("companion_id") != EXPECTED_COMPANION_ID:
            return None

        health = float(state.get("health", 0))

        state["health_status"] = get_health_status(health)

        return state

    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return None