import requests

from prompts import COMPANION_PROMPT
from config import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL
from memory import remember, load_memory
from ai_extractor import extract_memory_with_ai


def build_messages(message, history):
    messages = [
        {
            "role": "system",
            "content": COMPANION_PROMPT
        }
    ]

    memory = load_memory()

    if memory:
        memory_text = "Known facts about the user:\n"

        for key, value in memory.items():
            memory_text += f"- {key}: {value}\n"

        messages.append(
            {
                "role": "system",
                "content": memory_text
            }
        )

    for item in history:
        role = item["role"]
        content = item["content"]

        if isinstance(content, list):
            content = content[0]["text"]

        if role in ["user", "assistant"]:
            messages.append(
                {
                    "role": role,
                    "content": content
                }
            )

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    return messages


def ask_lm_studio(messages):
    url = f"{LM_STUDIO_BASE_URL}/chat/completions"

    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 120
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()


def ask_ai(message, history):
    memory = load_memory()

    facts = extract_memory_with_ai(message)

    for key, value in facts.items():
        remember(key, value)

    messages = build_messages(message, history)

    return ask_lm_studio(messages)