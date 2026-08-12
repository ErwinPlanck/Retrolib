import os
from pathlib import Path

from assets import get_assets
from get_files import get_files
from library import get_game_metadata
from retroarch_config import find_retroarch_executable

from .names import clean_game_name
from platforms import get_core_filename

ASSET_FIELDS = {
    "box_front": "assets.boxFront",
    "screenshot": "assets.screenshot",
    "titlescreen": "assets.titlescreen",
    "logo": "assets.logo",
    "marquee": "assets.marquee",
    "screenmarquee": "assets.bezel",
    "steamgrid": "assets.steamgrid",
    "video": "assets.video",
}

GAME_METADATA_FIELDS = {
    "developer": "developer",
    "publisher": "publisher",
    "genre": "genre",
    "release": "release",
    "players": "players",
    "description": "description",
    "platform": "platform",
}


def _relative_path(target: Path, start: Path) -> str:
    return os.path.relpath(
        target,
        start=start
    ).replace("\\", "/")


def generate_metadata(library, folders):

    metadata_root = folders["metadata"] / "Pegasus"
    metadata_root.mkdir(
        parents=True,
        exist_ok=True
    )

    retroarch_executable = find_retroarch_executable()

    if retroarch_executable is None:
        raise RuntimeError(
            "No se encontró el ejecutable de RetroArch"
        )

    for system in library["systems"]:

        system_folder = (
            folders["roms"] / system["name"]
        )

        if not system_folder.exists():
            continue

        files = get_files(
            system,
            system_folder
        )

        if not files:
            continue

        system_metadata_folder = (
            metadata_root / system["name"]
        )

        system_metadata_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        metadata_file = (
            system_metadata_folder
            / "metadata.pegasus.txt"
        )

        core_path = (
            folders["cores"]
            / get_core_filename(
                system["core_library"]
            )
        )

        lines = [
            f"collection: {system['name']}",
        ]

        for extension in system["extensions"]:
            lines.append(
                f"extension: {extension}"
            )

        lines.append(
            f'launch: "{retroarch_executable}" '
            f'-L "{core_path}" "{{file.path}}"'
        )

        lines.append("")

        for game in files:

            game_path = game["path"]
            game_label = game["label"]
            display_name = clean_game_name(game_label)

            game_metadata = get_game_metadata(
                library,
                game_label
            )

            assets = get_assets(
                game,
                system,
                folders
            )

            lines.append(
                f"game: {display_name}"
            )

            lines.append(
                f"file: {_relative_path(game_path, system_metadata_folder)}"
            )

            for asset_type, pegasus_field in ASSET_FIELDS.items():

                if asset_type not in assets:
                    continue

                asset_path = _relative_path(
                    assets[asset_type],
                    system_metadata_folder
                )

                lines.append(
                    f"{pegasus_field}: {asset_path}"
                )

            for metadata_key, pegasus_field in GAME_METADATA_FIELDS.items():

                if metadata_key not in game_metadata:
                    continue

                value = game_metadata[metadata_key]

                lines.append(
                    f"{pegasus_field}: {value}"
                )

            lines.append("")

        with open(
            metadata_file,
            "w",
            encoding="utf-8",
            newline="\n"
        ) as f:

            f.write(
                "\n".join(lines).rstrip() + "\n"
            )