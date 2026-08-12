import platform


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


if platform.system() == "Darwin":

    from .macos import (
        get_default_retroarch_cfg,
        get_retroarch_executable,
        get_default_pegasus_config_dirs
    )


elif platform.system() == "Windows":

    from .windows import (
        get_default_retroarch_cfg,
        get_retroarch_executable,
        get_default_pegasus_config_dirs
    )


else:

    raise RuntimeError(
        f"Sistema operativo no soportado: "
        f"{platform.system()}"
    )