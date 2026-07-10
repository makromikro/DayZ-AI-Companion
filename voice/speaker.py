import os
import subprocess
import tempfile
import time
import winsound


VOICE_MODEL = "en_GB-northern_english_male-medium.onnx"


def speak(text, measure=False):
    if not text:
        return None

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_path = temp_file.name
    temp_file.close()

    try:
        generation_start = time.perf_counter()

        subprocess.run(
            [
                "piper",
                "--model",
                VOICE_MODEL,
                "--output_file",
                temp_path
            ],
            input=text,
            text=True,
            check=True
        )

        generation_end = time.perf_counter()

        winsound.PlaySound(
            temp_path,
            winsound.SND_FILENAME
        )

        playback_end = time.perf_counter()

        if measure:
            return {
                "generation": generation_end - generation_start,
                "playback": playback_end - generation_end
            }

    except Exception as error:
        print(f"TTS error: {error}")
        return None

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)