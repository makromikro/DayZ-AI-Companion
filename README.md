# 🧠 DayZ AI Companion

An AI-powered companion for **DayZ** that can listen, remember, and assist you in real time while you play.

## Features

- 🎤 Voice input using your microphone
- 📝 Speech-to-text with Faster Whisper
- 🧠 Local AI powered by LM Studio
- 💾 Persistent long-term memory
- ⚡ Fast responses (under 2 seconds)
- 🏗️ Modular architecture for future expansion

## Current Architecture

```
Microphone
      │
      ▼
Faster Whisper
      │
      ▼
Runtime
      │
      ▼
LM Studio (Qwen)
      │
      ▼
AI Response
```

## Tech Stack

- Python
- LM Studio
- Qwen 2.5
- Faster Whisper
- Gradio
- Requests
- NumPy
- SoundDevice

## Roadmap

### ✅ Completed

- Local AI backend
- LM Studio integration
- Persistent memory
- AI memory extraction
- Runtime
- Scheduler
- Decision Engine
- Voice input
- Speech-to-text

### 🚧 In Progress

- Continuous voice conversation
- Text-to-speech
- Improved memory system

### 🔜 Planned

- DayZ game integration
- Screen understanding
- Inventory awareness
- Map awareness
- Autonomous companion
- NPC interaction

## Project Status

Current Version: **v0.2.0**

The project is under active development.

## License

MIT