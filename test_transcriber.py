from voice.microphone import record_audio, save_wav
from voice.transcriber import transcribe_audio_file

audio = record_audio()
save_wav("test.wav", audio)

text = transcribe_audio_file("test.wav")

print("You said:")
print(text)