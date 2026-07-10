import subprocess
import tempfile
import winsound
import os


VOICE_MODEL = "en_GB-northern_english_male-medium.onnx"


def speak(text):
    """
    Convert text to speech with Piper and play the generated audio.
    """

    if not text:
        return

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_path = temp_file.name
    temp_file.close()

    try:
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

        winsound.PlaySound(
            temp_path,
            winsound.SND_FILENAME
        )

    except Exception as error:
        print(f"TTS error: {error}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)