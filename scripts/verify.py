from get_files import get_files


def verify_library(library, folders):

    roms_folder = folders["roms"]
    results = []

    for system in library["systems"]:

        system_folder = roms_folder / system["name"]

        if not system_folder.exists():

            results.append(
                {
                    "section": "Biblioteca",
                    "name": system["name"],
                    "exists": False,
                    "roms": 0
                }
            )

            continue

        games = get_files(
            system,
            system_folder
        )

        results.append(
            {
                "section": "Biblioteca",
                "name": system["name"],
                "exists": True,
                "roms": len(games)
            }
        )

    return results