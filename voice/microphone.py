import sounddevice as sd
import numpy as np
import wave

SAMPLE_RATE = 16000
DURATION_SECONDS = 5


def record_audio():
    print("Recording... Speak now.")

    audio = sd.rec(
        int(DURATION_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()
    print("Recording finished.")

    return np.squeeze(audio)


def save_wav(filename, audio):
    audio_int16 = (audio * 32767).astype(np.int16)

    with wave.open(filename, "wb") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(audio_int16.tobytes())