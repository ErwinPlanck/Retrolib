def verify_bios(library, folders):

    bios_folder = folders["bios"]
    results = []

    for system in library["systems"]:

        bios_config = system.get("bios")

        if not bios_config:
            continue

        missing = []

        for pattern in bios_config["files"]:

            matches = list(bios_folder.glob(pattern))

            if not matches:
                missing.append(pattern)

        results.append(
            {
                "section": "BIOS",
                "name": system["name"],
                "required": bios_config["required"],
                "exists": len(missing) == 0,
                "missing": missing
            }
        )

    return results