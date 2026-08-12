from pathlib import Path
import json

from platforms import (
    get_default_retroarch_cfg,
    get_retroarch_executable
)


def get_config_file():

    return (
        Path(__file__).parent.parent
        / "config.json"
    )


def load_config():

    config_file = get_config_file()

    if config_file.exists():

        try:

            with open(
                config_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except json.JSONDecodeError:

            raise RuntimeError(
                "El archivo config.json no contiene "
                "un JSON válido."
            )

    return {}


def save_config(config):

    config_file = get_config_file()

    config_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        config_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4,
            ensure_ascii=False
        )


def find_retroarch_executable(
    config,
    path=None
):

    # ---------------------------------------------
    # 1. Ruta proporcionada manualmente
    # ---------------------------------------------

    if path is not None:

        path = Path(path).expanduser()

        # Windows: retroarch.exe
        if (
            path.is_file()
            and path.name.lower()
            == "retroarch.exe"
        ):

            config["retroarch_executable"] = str(
                path.resolve()
            )

            save_config(config)

            return path.resolve()

        # macOS: ejecutable RetroArch
        if (
            path.is_file()
            and path.name == "RetroArch"
        ):

            config["retroarch_executable"] = str(
                path.resolve()
            )

            save_config(config)

            return path.resolve()

        # Si se proporciona una carpeta
        if path.is_dir():

            # Windows
            executable = (
                path / "retroarch.exe"
            )

            if executable.exists():

                config["retroarch_executable"] = str(
                    executable.resolve()
                )

                save_config(config)

                return executable.resolve()

            # macOS
            executable = (
                path
                / "Contents"
                / "MacOS"
                / "RetroArch"
            )

            if executable.exists():

                config["retroarch_executable"] = str(
                    executable.resolve()
                )

                save_config(config)

                return executable.resolve()

    # ---------------------------------------------
    # 2. Ruta guardada en config.json
    # ---------------------------------------------

    saved_path = config.get(
        "retroarch_executable"
    )

    if saved_path:

        executable = Path(
            saved_path
        ).expanduser()

        if executable.exists():

            return executable.resolve()

    # ---------------------------------------------
    # 3. Detección automática
    # ---------------------------------------------

    executable = get_retroarch_executable()

    if executable is not None:

        config["retroarch_executable"] = str(
            executable.resolve()
        )

        save_config(config)

        return executable.resolve()

    return None


def find_retroarch(
    config,
    path=None
):

    # ---------------------------------------------
    # 1. Ruta proporcionada manualmente
    # ---------------------------------------------

    if path is not None:

        path = Path(path).expanduser()

        # El usuario proporcionó directamente
        # retroarch.cfg
        if (
            path.is_file()
            and path.name.lower()
            == "retroarch.cfg"
        ):

            config["retroarch_cfg"] = str(
                path.resolve()
            )

            save_config(config)

            return path.resolve()

        # El usuario proporcionó una carpeta
        if path.is_dir():

            retroarch_cfg = (
                path / "retroarch.cfg"
            )

            if retroarch_cfg.exists():

                config["retroarch_cfg"] = str(
                    retroarch_cfg.resolve()
                )

                save_config(config)

                return retroarch_cfg.resolve()

    # ---------------------------------------------
    # 2. Ruta guardada en config.json
    # ---------------------------------------------

    saved_path = config.get(
        "retroarch_cfg"
    )

    if saved_path:

        retroarch_cfg = Path(
            saved_path
        ).expanduser()

        if retroarch_cfg.exists():

            return retroarch_cfg.resolve()

    # ---------------------------------------------
    # 3. Detección automática
    # ---------------------------------------------

    for retroarch_cfg in get_default_retroarch_cfg():

        if retroarch_cfg.exists():

            config["retroarch_cfg"] = str(
                retroarch_cfg.resolve()
            )

            save_config(config)

            return retroarch_cfg.resolve()

    return None