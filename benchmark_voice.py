import time

from voice.microphone import record_audio, save_wav
from voice.transcriber import transcribe_audio_file
from voice.speaker import speak
from core.runtime import process_message


def main():
    history = []

    audio = record_audio()
    save_wav("voice_input.wav", audio)

    start = time.perf_counter()

    text = transcribe_audio_file("voice_input.wav")
    after_transcription = time.perf_counter()

    answer = process_message(text, history)
    after_ai = time.perf_counter()

    tts_times = speak(answer, measure=True)

    print("\nYou said:")
    print(text)

    print("\nCompanion:")
    print(answer)

    print("\nLatency:")
    print(f"Speech-to-text: {after_transcription - start:.2f}s")
    print(f"AI processing: {after_ai - after_transcription:.2f}s")

    if tts_times:
        print(f"TTS generation: {tts_times['generation']:.2f}s")
        print(f"Audio playback: {tts_times['playback']:.2f}s")
        print(
            "Time until speech starts: "
            f"{after_ai - start + tts_times['generation']:.2f}s"
        )


if __name__ == "__main__":
    main()