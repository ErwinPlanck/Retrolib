from pathlib import Path
import os


def get_default_retroarch_cfg():

    candidates = []

    appdata = os.environ.get(
        "APPDATA"
    )

    if appdata:

        candidates.extend(
            [
                Path(appdata)
                / "retroarch.cfg",

                Path(appdata)
                / "RetroArch"
                / "retroarch.cfg",

                Path(appdata)
                / "RetroArch"
                / "config"
                / "retroarch.cfg",
            ]
        )

    return candidates


def get_retroarch_executable():

    candidates = [
        Path("C:/RetroArch/retroarch.exe"),
        Path("C:/RetroArch-Win64/retroarch.exe"),
        Path.home()
        / "RetroArch"
        / "retroarch.exe",
        Path.home()
        / "RetroArch-Win64"
        / "retroarch.exe",
    ]

    for executable in candidates:

        if executable.exists():
            return executable

    return None

def get_default_pegasus_config_dirs():

    candidates = []

    localappdata = os.environ.get(
        "LOCALAPPDATA"
    )

    if localappdata:

        candidates.append(
            Path(localappdata)
            / "pegasus-frontend"
        )

    programdata = os.environ.get(
        "PROGRAMDATA"
    )

    if programdata:

        candidates.append(
            Path(programdata)
            / "pegasus-frontend"
        )

    return candidates