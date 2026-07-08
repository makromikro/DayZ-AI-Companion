from voice.microphone import record_audio, save_wav
from voice.transcriber import transcribe_audio_file
from core.runtime import process_message


def main():
    history = []

    audio = record_audio()
    save_wav("voice_input.wav", audio)

    text = transcribe_audio_file("voice_input.wav")

    print("\nYou said:")
    print(text)

    answer = process_message(text, history)

    print("\nCompanion:")
    print(answer)


if __name__ == "__main__":
    main()