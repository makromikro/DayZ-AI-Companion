import sounddevice as sd
import numpy as np
import wave
import time


SAMPLE_RATE = 16000
CHANNELS = 1

# Audio is processed in small chunks.
BLOCK_DURATION = 0.1
BLOCK_SIZE = int(SAMPLE_RATE * BLOCK_DURATION)

# Speech detection settings.
SPEECH_THRESHOLD = 0.015
SILENCE_DURATION = 1.2
MAX_RECORDING_DURATION = 30

# How often the current audio level is printed while waiting.
DEBUG_AUDIO_LEVEL = False


def get_audio_level(audio):
    """
    Calculate the RMS volume level of an audio chunk.
    """

    return float(np.sqrt(np.mean(np.square(audio))))


def record_audio():
    """
    Wait for the user to start speaking, record while they speak,
    and stop automatically after a period of silence.
    """

    print("Listening... Speak when ready.")

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

            if DEBUG_AUDIO_LEVEL:
                print(f"Audio level: {audio_level:.5f}")

            # Wait until speech is detected.
            if not speech_started:
                if audio_level >= SPEECH_THRESHOLD:
                    speech_started = True
                    recording_start = time.time()
                    silence_start = None

                    recorded_chunks.append(audio_chunk.copy())

                    print("Speech detected. Recording...")

                continue

            # Speech has already started.
            recorded_chunks.append(audio_chunk.copy())

            if audio_level >= SPEECH_THRESHOLD:
                # User is still speaking.
                silence_start = None

            else:
                # Silence has started.
                if silence_start is None:
                    silence_start = time.time()

                silence_length = time.time() - silence_start

                if silence_length >= SILENCE_DURATION:
                    print("Silence detected. Recording finished.")
                    break

            recording_duration = time.time() - recording_start

            if recording_duration >= MAX_RECORDING_DURATION:
                print("Maximum recording duration reached.")
                break

    if not recorded_chunks:
        return np.array([], dtype=np.float32)

    return np.concatenate(recorded_chunks)


def save_wav(filename, audio):
    """
    Save recorded audio as a 16-bit mono WAV file.
    """

    if audio.size == 0:
        return

    audio = np.clip(audio, -1.0, 1.0)
    audio_int16 = (audio * 32767).astype(np.int16)

    with wave.open(filename, "wb") as file:
        file.setnchannels(CHANNELS)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(audio_int16.tobytes())