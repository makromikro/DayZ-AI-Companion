IMPORTANT_KEYS = {
    "player_name": 10,
    "country": 8,
    "age": 8,
    "eye_color": 6,
    "favorite_weapon": 9,
    "base_location": 10,
    "friends": 9,
    "goal": 10
}


def get_importance(key):
    """
    Returns the importance score of a memory.
    """

    return IMPORTANT_KEYS.get(key, 3)


def is_important(key, minimum_score=5):
    """
    Returns True if the memory should be stored.
    """

    return get_importance(key) >= minimum_score