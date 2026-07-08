from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")


def transcribe_audio_file(filename):
    segments, info = model.transcribe(filename)

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()