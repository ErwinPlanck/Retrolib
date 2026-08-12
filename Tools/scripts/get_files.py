from pathlib import Path


def _is_valid_file(path, extensions):
    if not path.is_file():
        return False

    return path.suffix.lower().lstrip(".") in {
        extension.lower().lstrip(".")
        for extension in extensions
    }


def _get_file_game(path):
    return {
        "path": path,
        "label": path.stem,
    }


def _get_folder_game(folder, extensions):
    files = sorted(
        (
            path
            for path in folder.iterdir()
            if _is_valid_file(path, extensions)
        ),
        key=lambda path: path.name.lower()
    )

    if not files:
        return None

    return {
        "path": files[0],
        "label": folder.name,
    }


def get_files(system, system_folder):

    extensions = system["extensions"]
    scan_mode = system.get("scan", "file").lower()

    if scan_mode == "file":

        files = sorted(
            (
                path
                for path in system_folder.iterdir()
                if _is_valid_file(path, extensions)
            ),
            key=lambda path: path.name.lower()
        )

        return [
            _get_file_game(path)
            for path in files
        ]

    if scan_mode == "folder":

        games = []

        folders = sorted(
            (
                path
                for path in system_folder.iterdir()
                if path.is_dir()
            ),
            key=lambda path: path.name.lower()
        )

        for folder in folders:

            game = _get_folder_game(
                folder,
                extensions
            )

            if game is not None:
                games.append(game)

        return games

    raise ValueError(
        f"Modo de escaneo no válido para "
        f"{system['name']!r}: {scan_mode!r}"
    )