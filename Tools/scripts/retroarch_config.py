from pathlib import Path

from library import RETROARCH_DIRECTORIES

def load_retroarch(retroarch_cfg):

    retroarch = {
        "config_file": retroarch_cfg
    }

    with open(
        retroarch_cfg,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            line = line.strip()

            if "=" in line:

                key, value = line.split(
                    "=",
                    1
                )

                key = key.strip()
                value = value.strip().strip('"')

                if value.startswith("~"):

                    value = str(
                        Path(value).expanduser()
                    )

                retroarch[key] = value

    return retroarch


def verify_retroarch(retroarch, folders):

    results = []

    for key, info in RETROARCH_DIRECTORIES.items():

        path = folders[info["folder"]]

        if "subfolder" in info:

            path /= info["subfolder"]

        results.append(
            {
                "section": "RetroArch",
                "name": info["name"],
                "exists": (
                    retroarch.get(key)
                    == str(path)
                )
            }
        )

    return results


def configure_retroarch(
    retroarch,
    folders
):

    for key, info in RETROARCH_DIRECTORIES.items():

        path = folders[info["folder"]]

        if "subfolder" in info:

            path /= info["subfolder"]

        retroarch[key] = str(path)

    return retroarch


def save_retroarch(retroarch):

    config_file = retroarch["config_file"]

    with open(
        config_file,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    for i, line in enumerate(lines):

        if "=" not in line:
            continue

        key = line.split(
            "=",
            1
        )[0].strip()

        if key in RETROARCH_DIRECTORIES:

            lines[i] = (
                f'{key} = "{retroarch[key]}"\n'
            )

    with open(
        config_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(lines)