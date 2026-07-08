import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):

    memory = load_memory()

    # Merge lists
    if isinstance(value, list):

        existing = memory.get(key, [])

        if not isinstance(existing, list):
            existing = [existing]

        for item in value:
            if item not in existing:
                existing.append(item)

        memory[key] = existing

    else:
        memory[key] = value

    save_memory(memory)