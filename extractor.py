def extract_memory(message):
    """
    Extract important facts from a user message.
    Returns a dictionary containing anything worth remembering.
    """

    facts = {}

    lower_message = message.lower()

    # Remember the player's name
    if "my name is" in lower_message:
        index = lower_message.find("my name is")
        name = message[index + len("my name is"):].strip().title()
        facts["player_name"] = name

    # Remember eye color
    if "my eyes are" in lower_message:
        index = lower_message.find("my eyes are")
        eye_color = message[index + len("my eyes are"):].strip().lower()
        facts["eye_color"] = eye_color

    # Remember where the player lives
    if "i live in" in lower_message:
        index = lower_message.find("i live in")
        country = message[index + len("i live in"):].strip().title()
        facts["country"] = country

    # Remember favorite weapon
    if "my favorite weapon is" in lower_message:
        index = lower_message.find("my favorite weapon is")
        weapon = message[index + len("my favorite weapon is"):].strip()
        facts["favorite_weapon"] = weapon

    return facts