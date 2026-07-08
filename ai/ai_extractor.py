import json
import re
import requests

from config import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL
from memory_system.memory_manager import clean_memory


def extract_memory_with_ai(message):
    prompt = f"""
You are an AI memory system.

Extract ONLY long-term facts about the user.

Remember things like:
- Name
- Age
- Country
- Eye color
- Favorite weapon
- Base location
- Friends
- Goals

Ignore temporary information.

Return ONLY valid JSON.

User:
{message}
"""

    messages = [
        {
            "role": "system",
            "content": "Return only valid JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    url = f"{LM_STUDIO_BASE_URL}/chat/completions"

    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 150
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        return {}

    try:
        memory = json.loads(match.group())
        return clean_memory(memory)

    except json.JSONDecodeError:
        return {}