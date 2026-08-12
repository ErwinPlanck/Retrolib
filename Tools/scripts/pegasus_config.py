from pathlib import Path

from platforms import (
    get_default_pegasus_config_dirs
)


def find_pegasus_config_dir():

    candidates = (
        get_default_pegasus_config_dirs()
    )

    for config_dir in candidates:

        if (
            (config_dir / "game_dirs.txt").exists()
            or
            (config_dir / "settings.txt").exists()
        ):
            return config_dir

    return (
        candidates[0]
        if candidates
        else None
    )


def load_game_dirs(game_dirs_file):

    if not game_dirs_file.exists():
        return []

    game_dirs = []

    with open(
        game_dirs_file,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if (
                line
                and not line.startswith("#")
            ):
                game_dirs.append(line)

    return game_dirs


def save_game_dirs(
    game_dirs_file,
    game_dirs
):

    game_dirs_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        game_dirs_file,
        "w",
        encoding="utf-8",
        newline="\n"
    ) as f:

        for directory in game_dirs:
            f.write(
                f"{directory}\n"
            )


def configure_pegasus(
    game_directories,
    config_dir=None
):

    if config_dir is None:

        config_dir = (
            find_pegasus_config_dir()
        )

    if config_dir is None:

        raise RuntimeError(
            "No se pudo determinar "
            "el directorio de configuración "
            "de Pegasus."
        )

    game_dirs_file = (
        config_dir / "game_dirs.txt"
    )

    existing_dirs = load_game_dirs(
        game_dirs_file
    )

    normalized = {
        str(
            Path(directory)
            .expanduser()
            .resolve()
        )
        for directory in existing_dirs
    }

    for game_directory in game_directories:

        target = str(
            Path(game_directory).resolve()
        )

        if target not in normalized:

            existing_dirs.append(
                target
            )

            normalized.add(target)

    save_game_dirs(
        game_dirs_file,
        existing_dirs
    )

    return game_dirs_file


def verify_pegasus(
    game_directory,
    config_dir=None
):

    if config_dir is None:

        config_dir = (
            find_pegasus_config_dir()
        )

    if config_dir is None:
        return False

    game_dirs_file = (
        config_dir / "game_dirs.txt"
    )

    target = str(
        Path(game_directory).resolve()
    )

    game_dirs = load_game_dirs(
        game_dirs_file
    )

    normalized = {
        str(
            Path(directory)
            .expanduser()
            .resolve()
        )
        for directory in game_dirs
    }

    return target in normalized