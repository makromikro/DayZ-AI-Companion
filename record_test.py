from voice.microphone import record_audio, save_wav

audio = record_audio()
save_wav("test.wav", audio)

print("Saved test.wav")