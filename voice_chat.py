import threading
import time

from core.runtime import process_message
from dayz.event_monitor import DayZEventMonitor
from dayz.speech_writer import write_speech_command
from dayz.state_reader import load_companion_state
from voice.microphone import record_audio, save_wav
from voice.speaker import speak
from voice.transcriber import transcribe_audio_file


EXIT_WORDS = {"goodbye", "exit", "quit"}
VOICE_INPUT_FILE = "voice_input.wav"

EVENT_CHECK_INTERVAL = 1.0

event_monitor = DayZEventMonitor(
    warning_distance=35.0,
    danger_distance=15.0,
    warning_cooldown=20.0,
)

stop_event = threading.Event()
speech_lock = threading.Lock()


def should_exit(text):
    words = {
        word.strip(".,!?").lower()
        for word in text.split()
    }

    return bool(words & EXIT_WORDS)


def build_infected_warning(event):
    infected_count = int(event["infected_count"])
    distance = round(float(event["distance"]))
    reason = event["reason"]

    if reason == "immediate_danger":
        if infected_count == 1:
            return f"Infected close, about {distance} metres."

        return (
            f"{infected_count} infected close, "
            f"nearest about {distance} metres."
        )

    if reason == "count_increased":
        return (
            f"More infected nearby. "
            f"{infected_count} within range."
        )

    if reason == "approaching":
        if infected_count == 1:
            return f"That infected is closing in, about {distance} metres."

        return (
            f"They're getting closer, "
            f"nearest about {distance} metres."
        )

    if infected_count == 1:
        return f"Infected nearby, about {distance} metres."

    return (
        f"{infected_count} infected nearby, "
        f"nearest about {distance} metres."
    )


def speak_as_boris(text, label="Companion"):
    """
    Send Boris's text to DayZ and speak it without allowing
    another Boris voice line to overlap.
    """

    if not text:
        return

    with speech_lock:
        print(f"\n{label}:")
        print(text)

        write_speech_command(text)
        speak(text)


def event_monitor_loop():
    """
    Continuously monitor live DayZ state in the background.
    """

    while not stop_event.is_set():
        try:
            state = load_companion_state()
            event = event_monitor.check(state)

            if event:
                warning = build_infected_warning(event)
                speak_as_boris(warning, label="Boris warning")

        except Exception as error:
            print(f"\nEvent monitor error: {error}")

        stop_event.wait(EVENT_CHECK_INTERVAL)


def main():
    history = []

    monitor_thread = threading.Thread(
        target=event_monitor_loop,
        name="dayz-event-monitor",
        daemon=True,
    )

    monitor_thread.start()

    print("DayZ AI Companion started.")
    print("Say 'goodbye', 'exit', or 'quit' to stop.")

    try:
        while not stop_event.is_set():
            audio = record_audio()

            if stop_event.is_set():
                break

            if audio.size == 0:
                print("No audio recorded.")
                continue

            save_wav(VOICE_INPUT_FILE, audio)

            text = transcribe_audio_file(VOICE_INPUT_FILE)

            if not text:
                print("No speech detected.")
                continue

            print("\nYou said:")
            print(text)

            if should_exit(text):
                speak_as_boris("Goodbye.")
                break

            answer = process_message(text, history)

            speak_as_boris(answer)

            history.append(
                {
                    "role": "user",
                    "content": text,
                }
            )

            history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

    except KeyboardInterrupt:
        print("\nStopping companion...")

    finally:
        stop_event.set()
        monitor_thread.join(timeout=2.0)
        print("Companion stopped.")


if __name__ == "__main__":
    main()