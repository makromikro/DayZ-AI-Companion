from faster_whisper import WhisperModel


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def transcribe_audio_file(filename):
    segments, _ = model.transcribe(
        filename,
        beam_size=1,
        vad_filter=False
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()