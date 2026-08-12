from platforms import get_core_filename

def verify_cores(library, folders):

    cores_folder = folders["cores"]
    results = []

    for system in library["systems"]:

        core_file = (
            cores_folder
            / get_core_filename(
                system["core_library"]
            )
        )

        results.append(
            {
                "section": "Nucleos",
                "name": system["name"],
                "core": system["core"],
                "exists": core_file.exists()
            }
        )

    return results