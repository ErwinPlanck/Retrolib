from pathlib import Path
import json

from generate_library import generate_library


RETROARCH_DIRECTORIES = {
    "playlist_directory": {
        "name": "Playlist Directory",
        "folder": "metadata",
        "subfolder": "RetroArch"
    },
    "system_directory": {
        "name": "BIOS Directory",
        "folder": "bios"
    },
    "savefile_directory": {
        "name": "Savefile Directory",
        "folder": "saves"
    },
    "savestate_directory": {
        "name": "Savestate Directory",
        "folder": "states"
    },
    "thumbnails_directory": {
        "name": "Thumbnail Directory",
        "folder": "thumbnails"
    },
    "libretro_directory": {
        "name": "Core Directory",
        "folder": "cores"
    },
    "libretro_info_path": {
        "name": "Core Info Directory",
        "folder": "core_info"
    }
}


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def load_library():

    script_folder = Path(__file__).parent
    tools_folder = script_folder.parent
    root = tools_folder.parent

    # RetroLib/Tools/data/
    data_folder = tools_folder / "data"

    systems_file = (
        data_folder / "systems.json"
    )

    library_file = (
        data_folder / "library.json"
    )

    roms_folder = (
        root / "ROMs"
    )

    gamelists_folder = (
        root / "gamelists"
    )

    # Generar library.json a partir de:
    # systems.json + ROMs + gamelists.
    generate_library(
        systems_file,
        roms_folder,
        gamelists_folder,
        library_file
    )

    # Cargar catálogo maestro.
    systems_data = load_json(
        systems_file
    )

    # Cargar biblioteca generada.
    library = load_json(
        library_file
    )

    all_systems = systems_data.get(
        "systems",
        []
    )

    systems_by_name = {
        system["name"]: system
        for system in all_systems
    }

    library_systems = []

    for system_name in library.get(
        "systems",
        []
    ):

        system = systems_by_name.get(
            system_name
        )

        if system is None:
            continue

        library_systems.append(
            system
        )

    # Sustituir los nombres de los sistemas
    # por sus definiciones completas.
    library["systems"] = library_systems

    folders = {
        "root": root,
        "roms": root / "ROMs",
        "metadata": root / "Metadata",
        "bios": root / "BIOS",
        "cores": root / "Cores",
        "core_info": root / "CoreInfo",
        "assets": root / "Assets",
        "thumbnails": root / "Thumbnails",
        "saves": root / "Saves",
        "states": root / "SaveStates"
    }

    return library, folders


def get_game_metadata(
    library,
    game_label
):

    games = library.get(
        "games",
        {}
    )

    return games.get(
        game_label,
        {}
    )