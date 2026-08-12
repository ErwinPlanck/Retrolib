import json

from get_files import get_files
from .names import clean_game_name
from platforms import get_core_filename


def generate_playlists(library, folders):

    playlists_folder = (
        folders["metadata"] / "RetroArch"
    )

    playlists_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    for system in library["systems"]:

        system_folder = (
            folders["roms"] / system["name"]
        )

        if not system_folder.exists():
            continue

        core_path = (
            folders["cores"]
            / get_core_filename(
                system["core_library"]
            )
        )

        playlist_file = (
            playlists_folder
            / f"{system['playlist']}.lpl"
        )

        files = get_files(
            system,
            system_folder
        )

        playlist = {
            "version": "1.5",
            "default_core_path": str(core_path),
            "default_core_name": system["core_name"],
            "label_display_mode": 0,
            "right_thumbnail_mode": 0,
            "left_thumbnail_mode": 0,
            "thumbnail_match_mode": 0,
            "sort_mode": 0,
            "scan_content_dir": str(system_folder),
            "scan_file_exts": "",
            "scan_dat_file_path": "",
            "scan_database_name": "",
            "scan_search_recursively": True,
            "scan_search_archives": True,
            "scan_filter_dat_content": False,
            "scan_omit_db_ref": False,
            "scan_overwrite_playlist": False,
            "scan_db_usage": 0,
            "items": []
        }

        for game in files:

            playlist["items"].append(
                {
                    "path": str(game["path"]),
                    "label": clean_game_name(
                        game["label"]
                    ),
                    "core_name": system["core_name"],
                    "core_path": str(core_path),
                    "crc32": "DETECT",
                    "db_name": f"{system['playlist']}.lpl"
                }
            )

        with open(
            playlist_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                playlist,
                f,
                indent=2,
                ensure_ascii=False
            )