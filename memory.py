import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    """
    Load memory from disk.
    """

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)


def save_memory(memory):
    """
    Save memory to disk.
    """

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):
    """
    Save a single fact into long-term memory.
    """

    memory = load_memory()

    memory[key] = value

    save_memory(memory)
        