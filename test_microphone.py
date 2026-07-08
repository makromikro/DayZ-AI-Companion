from voice.microphone import record_audio

audio = record_audio()

print(type(audio))
print(audio.shape)
print(audio[:10])