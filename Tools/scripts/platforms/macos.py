from pathlib import Path


def get_default_retroarch_cfg():

    return [
        Path.home()
        / "Library/Application Support/RetroArch/config/retroarch.cfg",
        Path(
            "/Applications/RetroArch.app/"
            "Contents/MacOS/retroarch.cfg"
        ),
    ]


def get_retroarch_executable():

    candidates = [
        Path(
            "/Applications/RetroArch.app/"
            "Contents/MacOS/RetroArch"
        ),
        Path.home()
        / "Applications"
        / "RetroArch.app"
        / "Contents"
        / "MacOS"
        / "RetroArch",
    ]

    for executable in candidates:

        if executable.exists():
            return executable

    return None

def get_default_pegasus_config_dirs():

    return [
        Path.home()
        / "Library/Preferences/pegasus-frontend",

        Path.home()
        / "Library/Application Support/pegasus-frontend",

        Path(
            "/Library/Application Support/pegasus-frontend"
        ),
    ]