from memory_system.importance import is_important


def clean_memory(memory):
    """
    Clean and normalize AI memory before saving.
    """

    key_mapping = {
        "name": "player_name",
        "username": "player_name",
        "user_name": "player_name",
        "weapon": "favorite_weapon",
        "favorite_gun": "favorite_weapon",
        "gun": "favorite_weapon",
        "location": "base_location"
    }

    cleaned = {}

    for key, value in memory.items():

        key = key_mapping.get(key, key)

        if not is_important(key):
            continue

        if value is None:
            continue

        if isinstance(value, str):
            value = value.strip()

            if value == "":
                continue

        if key in cleaned:

            if isinstance(cleaned[key], list):

                if isinstance(value, list):
                    for item in value:
                        if item not in cleaned[key]:
                            cleaned[key].append(item)
                else:
                    if value not in cleaned[key]:
                        cleaned[key].append(value)

            else:
                cleaned[key] = value

        else:
            cleaned[key] = value

    return cleaned