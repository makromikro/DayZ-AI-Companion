import time
import wave
from collections import deque

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 16000
CHANNELS = 1

BLOCK_DURATION = 0.1
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

SPEECH_THRESHOLD = 0.015
SILENCE_DURATION = 1.2
MAX_RECORDING_DURATION = 30

# Keep one second of audio before speech is detected.
PRE_ROLL_DURATION = 1.0
PRE_ROLL_BLOCKS = int(PRE_ROLL_DURATION / BLOCK_DURATION)


def get_audio_level(audio):
    return float(np.sqrt(np.mean(np.square(audio))))


def record_audio():
    print("Listening... Speak when ready.")

    pre_roll = deque(maxlen=PRE_ROLL_BLOCKS)
    recorded_chunks = []

    speech_started = False
    silence_start = None
    recording_start = None

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        blocksize=BLOCK_SIZE
    ) as stream:

        while True:
            audio_chunk, overflowed = stream.read(BLOCK_SIZE)

            if overflowed:
                print("Warning: Audio input overflow.")

            audio_chunk = audio_chunk.flatten()
            audio_level = get_audio_level(audio_chunk)

            if not speech_started:
                pre_roll.append(audio_chunk.copy())

                if audio_level >= SPEECH_THRESHOLD:
                    speech_started = True
                    recording_start = time.time()
                    silence_start = None

                    # Include audio captured before detection.
                    recorded_chunks.extend(pre_roll)

                    print("Speech detected. Recording...")

                continue

            recorded_chunks.append(audio_chunk.copy())

            if audio_level >= SPEECH_THRESHOLD:
                silence_start = None
            else:
                if silence_start is None:
                    silence_start = time.time()

                if time.time() - silence_start >= SILENCE_DURATION:
                    print("Silence detected. Recording finished.")
                    break

            if time.time() - recording_start >= MAX_RECORDING_DURATION:
                print("Maximum recording duration reached.")
                break

    if not recorded_chunks:
        return np.array([], dtype=np.float32)

    return np.concatenate(recorded_chunks)


def save_wav(filename, audio):
    if audio.size == 0:
        return

    audio = np.clip(audio, -1.0, 1.0)
    audio_int16 = (audio * 32767).astype(np.int16)

    with wave.open(filename, "wb") as file:
        file.setnchannels(CHANNELS)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(audio_int16.tobytes())