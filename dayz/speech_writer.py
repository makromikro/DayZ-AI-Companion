import json
import time
from pathlib import Path


SPEECH_FILE = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\DayZServer"
    r"\profiles_ai_companion\DayZAICompanion\speech_command.json"
)

COMPANION_ID = "burak_companion_001"


def write_speech_command(text):
    SPEECH_FILE.parent.mkdir(parents=True, exist_ok=True)

    command = {
        "companion_id": COMPANION_ID,
        "speech_id": str(time.time_ns()),
        "text": text,
        "status": "pending",
    }

    temp_file = SPEECH_FILE.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as file:
        json.dump(command, file, indent=2, ensure_ascii=False)

    temp_file.replace(SPEECH_FILE)

    return command