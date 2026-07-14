import math
import os
import subprocess
import tempfile
import time
import wave

import numpy as np
import sounddevice as sd

from dayz.state_reader import load_companion_state


VOICE_MODEL = "en_GB-northern_english_male-medium.onnx"

MAX_HEARING_DISTANCE = 35.0
MIN_VOLUME = 0.08
MAX_PAN = 0.85


def calculate_volume(distance):
    if distance is None:
        return 1.0

    distance = float(distance)

    if distance >= MAX_HEARING_DISTANCE:
        return 0.0

    volume = 1.0 - (distance / MAX_HEARING_DISTANCE)

    return max(MIN_VOLUME, min(1.0, volume))


def normalize_2d(x, z):
    length = math.sqrt((x * x) + (z * z))

    if length <= 0.0001:
        return 0.0, 0.0

    return x / length, z / length


def calculate_pan(state):
    if not state:
        return 0.0

    companion = state.get("companion_position", {})
    player = state.get("player_position", {})
    direction = state.get("player_direction", {})

    companion_x = float(companion.get("x", 0.0))
    companion_z = float(companion.get("z", 0.0))

    player_x = float(player.get("x", 0.0))
    player_z = float(player.get("z", 0.0))

    direction_x = float(direction.get("x", 0.0))
    direction_z = float(direction.get("z", 1.0))

    to_boris_x = companion_x - player_x
    to_boris_z = companion_z - player_z

    to_boris_x, to_boris_z = normalize_2d(
        to_boris_x,
        to_boris_z,
    )

    direction_x, direction_z = normalize_2d(
        direction_x,
        direction_z,
    )

    right_x = direction_z
    right_z = -direction_x

    pan = (to_boris_x * right_x) + (to_boris_z * right_z)

    return max(-MAX_PAN, min(MAX_PAN, pan))


def apply_spatial_audio(audio, volume, pan):
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    left_gain = volume * math.sqrt((1.0 - pan) / 2.0)
    right_gain = volume * math.sqrt((1.0 + pan) / 2.0)

    left = audio * left_gain
    right = audio * right_gain

    stereo = np.column_stack((left, right))

    return np.clip(stereo, -1.0, 1.0)


def load_wav(filename):
    with wave.open(filename, "rb") as wav_file:
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        frame_count = wav_file.getnframes()

        if sample_width != 2:
            raise ValueError("Only 16-bit PCM WAV files are supported.")

        raw_audio = wav_file.readframes(frame_count)

    audio = np.frombuffer(raw_audio, dtype=np.int16)
    audio = audio.astype(np.float32) / 32768.0

    if channels > 1:
        audio = audio.reshape(-1, channels)

    return audio, sample_rate


def speak(text, measure=False):
    if not text:
        return None

    companion_state = load_companion_state()

    distance = None

    if companion_state:
        distance = companion_state.get("distance_to_player")

    volume = calculate_volume(distance)

    if volume <= 0:
        print("Boris is too far away to hear.")
        return None

    pan = calculate_pan(companion_state)

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False,
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
                temp_path,
            ],
            input=text,
            text=True,
            check=True,
        )

        generation_end = time.perf_counter()

        audio, sample_rate = load_wav(temp_path)

        spatial_audio = apply_spatial_audio(
            audio,
            volume,
            pan,
        )

        playback_start = time.perf_counter()

        sd.play(
            spatial_audio,
            samplerate=sample_rate,
        )
        sd.wait()

        playback_end = time.perf_counter()

        side = "center"

        if pan < -0.15:
            side = "left"
        elif pan > 0.15:
            side = "right"

        if distance is not None:
            print(
                f"Boris voice distance: {float(distance):.1f} m | "
                f"volume: {volume:.2f} | "
                f"pan: {pan:.2f} ({side})"
            )

        if measure:
            return {
                "generation": generation_end - generation_start,
                "playback": playback_end - playback_start,
            }

        return None

    except Exception as error:
        print(f"TTS error: {error}")
        return None

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)