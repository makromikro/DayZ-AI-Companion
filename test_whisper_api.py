import requests

url = "http://127.0.0.1:1234/v1/audio/transcriptions"

files = {
    "file": ("test.wav", open("test.wav", "rb"), "audio/wav")
}

data = {
    "model": "whisper-large-v3-turbo"
}

response = requests.post(url, files=files, data=data)

print(response.status_code)
print(response.text)