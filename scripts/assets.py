from pathlib import Path

ASSET_DIRECTORIES = {
    "box_3d": "3dboxes",
    "box_back": "backcovers",
    "box_front": "covers",
    "fanart": "fanart",
    "manual": "manuals",
    "marquee": "marquees",
    "miximage": "miximages",
    "physical_media": "physicalmedia",
    "screenshot": "screenshots",
    "titlescreen": "titlescreens",
    "video": "videos",
}


def create_asset_directories(system, folders):

    assets_folder = folders["assets"] / system["name"]

    for directory in ASSET_DIRECTORIES.values():
        (assets_folder / directory).mkdir(parents=True, exist_ok=True)

    return assets_folder


def get_assets(game, system, folders):

    assets_folder = folders["assets"] / system["name"]
    assets = {}

    for asset_type, directory in ASSET_DIRECTORIES.items():

        asset_folder = assets_folder / directory

        if not asset_folder.exists():
            continue

        for file in asset_folder.iterdir():

            if file.is_file() and file.stem == game["label"]:
                assets[asset_type] = file
                break

    return assets