from pathlib import Path
import os

def get_default_pegasus_config_dirs():

    dirs = []

    localappdata = os.environ.get(
        "LOCALAPPDATA"
    )

    if localappdata:
        dirs.append(
            Path(localappdata)
            / "pegasus-frontend"
        )

    programdata = os.environ.get(
        "PROGRAMDATA"
    )

    if programdata:
        dirs.append(
            Path(programdata)
            / "pegasus-frontend"
        )

    return dirs

def get_default_pegasus_config():

    localappdata = os.getenv("LOCALAPPDATA")

    if localappdata is None:
        return []

    return [
        Path(localappdata)
        / "pegasus-frontend"
        / "settings.txt"
    ]

def get_default_retroarch_cfg():

    appdata = os.getenv("APPDATA")

    if appdata is None:
        return []

    return [
        Path(appdata) / "retroarch.cfg",
        Path(appdata) / "RetroArch" / "retroarch.cfg",
        Path(appdata) / "RetroArch" / "config" / "retroarch.cfg"
    ]


def get_retroarch_executable():

    candidates = []

    appdata = os.getenv("APPDATA")

    if appdata is not None:

        candidates.append(
            Path(appdata)
            / "RetroArch"
            / "retroarch.exe"
        )

    candidates.extend(
        [
            Path("C:/RetroArch/retroarch.exe"),
            Path("C:/Program Files/RetroArch/retroarch.exe"),
            Path("C:/Program Files (x86)/RetroArch/retroarch.exe"),
            Path.home() / "RetroArch" / "retroarch.exe",
        ]
    )

    for executable in candidates:

        if executable.exists():
            return executable

    return None