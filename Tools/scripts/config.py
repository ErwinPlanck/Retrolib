from pathlib import Path
import json

from platforms import get_default_retroarch_cfg


def load_config():

    config_file = (
        Path(__file__).parent.parent
        / "config.json"
    )

    if config_file.exists():

        with open(
            config_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    return {}


def save_config(config):

    config_file = (
        Path(__file__).parent.parent
        / "config.json"
    )

    with open(
        config_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            config,
            f,
            indent=4
        )


def find_retroarch(config, folder=None):

    if folder is not None:

        retroarch_cfg = (
            Path(folder)
            / "retroarch.cfg"
        )

        if retroarch_cfg.exists():

            config["retroarch_cfg"] = (
                str(retroarch_cfg)
            )

            save_config(config)

            return retroarch_cfg

    if "retroarch_cfg" in config:

        retroarch_cfg = Path(
            config["retroarch_cfg"]
        )

        if retroarch_cfg.exists():
            return retroarch_cfg

    for retroarch_cfg in get_default_retroarch_cfg():

        if retroarch_cfg.exists():

            config["retroarch_cfg"] = (
                str(retroarch_cfg)
            )

            save_config(config)

            return retroarch_cfg

    return None