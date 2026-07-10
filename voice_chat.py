from voice.microphone import record_audio, save_wav
from voice.transcriber import transcribe_audio_file
from voice.speaker import speak
from core.runtime import process_message


EXIT_WORDS = {"goodbye", "exit", "quit"}


def should_exit(text):
    words = {
        word.strip(".,!?").lower()
        for word in text.split()
    }

    return bool(words & EXIT_WORDS)


def main():
    history = []

    print("DayZ AI Companion started.")
    print("Say 'goodbye', 'exit', or 'quit' to stop.")

    while True:
        audio = record_audio()
        save_wav("voice_input.wav", audio)

        text = transcribe_audio_file("voice_input.wav")

        if not text:
            print("No speech detected.")
            continue

        print("\nYou said:")
        print(text)

        if should_exit(text):
            print("Companion stopped.")
            speak("Goodbye.")
            break

        answer = process_message(text, history)

        print("\nCompanion:")
        print(answer)

        speak(answer)

        history.append(
            {
                "role": "user",
                "content": text
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


if __name__ == "__main__":
    main()