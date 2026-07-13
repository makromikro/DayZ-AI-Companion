import requests

from dayz.speech_writer import write_speech_command
from ai.prompts import COMPANION_PROMPT
from config import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL
from memory_system.memory import remember, load_memory
from ai.ai_extractor import extract_memory_with_ai
from dayz.state_reader import load_companion_state


MEMORY_PHRASES = (
    "my name is",
    "i am ",
    "i'm ",
    "i live in",
    "my favorite",
    "my friend",
    "my friends",
    "my base",
    "remember that",
    "i prefer",
    "i like",
    "i dislike",
    "i hate",
    "my goal",
)


def should_extract_memory(message):
    lower_message = message.lower()
    return any(phrase in lower_message for phrase in MEMORY_PHRASES)


def build_messages(message, history):
    messages = [
        {
            "role": "system",
            "content": COMPANION_PROMPT,
        }
    ]

    # Load long-term memory about the player
    memory = load_memory()

    if memory:
        memory_text = "Known facts about the player:\n"

        for key, value in memory.items():
            memory_text += f"- {key}: {value}\n"

        messages.append(
            {
                "role": "system",
                "content": memory_text,
            }
        )

    # Load live DayZ companion state
    companion_state = load_companion_state()

    if companion_state:
        position = companion_state.get("position", {})
        health = companion_state.get("health", "unknown")
        health_status = companion_state.get("health_status", "unknown")
        npc_type = companion_state.get("type", "unknown")

        state_text = (
            "Current live in-game state of your physical DayZ NPC body:\n"
            f"- NPC type: {npc_type}\n"
            f"- Health: {health}\n"
            f"- Health status: {health_status}\n"
            f"- Position: "
            f"x={position.get('x', 'unknown')}, "
            f"y={position.get('y', 'unknown')}, "
            f"z={position.get('z', 'unknown')}\n\n"
            "Important rules:\n"
            "- This is your own live in-game body state.\n"
            "- If asked about your health, answer using this live state.\n"
            "- Health status 'dead' means you are dead.\n"
            "- Health status 'critical' means you are critically injured.\n"
            "- Health status 'badly injured' means you are badly injured.\n"
            "- Health status 'injured' means you are injured.\n"
            "- Health status 'healthy' means you are in good health.\n"
            "- Do not invent bleeding, broken bones, hunger, thirst, or other conditions unless they are explicitly provided in the live game state.\n"
            "- Keep spoken responses short and natural."
        )

        messages.append(
            {
                "role": "system",
                "content": state_text,
            }
        )

    # Add recent conversation history
    for item in history:
        role = item["role"]
        content = item["content"]

        if isinstance(content, list):
            content = content[0]["text"]

        if role in ["user", "assistant"]:
            messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )

    # Add current user message
    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    return messages


def clean_ai_response(text):
    unwanted_markers = [
        "\nUser:",
        "\nUser",
        "\nAssistant:",
        "\nAssistant",
    ]

    for marker in unwanted_markers:
        if marker in text:
            text = text.split(marker, 1)[0]

    return text.strip()


def ask_lm_studio(messages):
    url = f"{LM_STUDIO_BASE_URL}/chat/completions"

    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 40,
    }

    response = requests.post(
        url,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    return clean_ai_response(answer)


def ask_ai(message, history):
    if should_extract_memory(message):
        facts = extract_memory_with_ai(message)

        for key, value in facts.items():
            remember(key, value)

    messages = build_messages(message, history)

    answer = ask_lm_studio(messages)

    write_speech_command(answer)

    return answer