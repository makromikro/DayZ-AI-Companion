def extract_memory(message):
    """
    Extract important facts from a user message.
    Returns a dictionary.
    """

    message = message.lower()

    if "my name is" in message:
        name = message.split("my name is")[-1].strip().title()
        return {
            "player_name": name
        }

    return {}