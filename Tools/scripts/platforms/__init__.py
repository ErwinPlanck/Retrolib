import platform

from . import macos
from . import windows

def get_default_pegasus_config_dirs():

    system = platform.system()

    if system == "Darwin":
        return macos.get_default_pegasus_config_dirs()

    if system == "Windows":
        return windows.get_default_pegasus_config_dirs()

    raise RuntimeError(
        f"Sistema operativo no soportado: {system}"
    )

def get_default_pegasus_config():

    system = platform.system()

    if system == "Darwin":
        return macos.get_default_pegasus_config()

    if system == "Windows":
        return windows.get_default_pegasus_config()

    raise RuntimeError(
        f"Sistema operativo no soportado: {system}"
    )

def get_core_extension():

    system = platform.system()

    if system == "Darwin":
        return ".dylib"

    if system == "Windows":
        return ".dll"

    if system == "Linux":
        return ".so"

    raise RuntimeError(
        f"Sistema operativo no soportado: {system}"
    )


def get_core_filename(core_library):

    return (
        core_library
        + get_core_extension()
    )


def get_default_retroarch_cfg():

    system = platform.system()

    if system == "Darwin":
        return macos.get_default_retroarch_cfg()

    if system == "Windows":
        return windows.get_default_retroarch_cfg()

    raise RuntimeError(
        f"Sistema operativo no soportado: {system}"
    )


def get_retroarch_executable():

    system = platform.system()

    if system == "Darwin":
        return macos.get_retroarch_executable()

    if system == "Windows":
        return windows.get_retroarch_executable()

    raise RuntimeError(
        f"Sistema operativo no soportado: {system}"
    )