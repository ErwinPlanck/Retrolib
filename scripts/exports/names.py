import re


def clean_game_name(name):
    return re.sub(r"\s*\([^)]*\)", "", name).strip()