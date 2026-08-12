import json
import sys
from pathlib import Path
from xml.etree import ElementTree


GAME_METADATA_FIELDS = {
    "developer": "developer",
    "publisher": "publisher",
    "genre": "genre",
    "releasedate": "release",
    "players": "players",
    "rating": "rating",
    "desc": "description",
}


def load_json(path):
    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def load_gamelist(path):
    """
    Carga un gamelist.xml y devuelve metadata
    indexada por el nombre exacto del archivo de ROM.
    """

    games = {}

    if not path.exists():
        return games

    try:
        tree = ElementTree.parse(path)

    except ElementTree.ParseError as error:
        print(
            f"Advertencia: no se pudo leer "
            f"{path}: {error}"
        )
        return games

    root = tree.getroot()

    for game in root.findall("game"):

        path_element = game.find("path")

        if path_element is None:
            continue

        if path_element.text is None:
            continue

        xml_path = path_element.text.strip()

        if not xml_path:
            continue

        # ./Game.nes → Game.nes
        filename = Path(xml_path).name

        metadata = {}

        for xml_field, library_field in GAME_METADATA_FIELDS.items():

            element = game.find(xml_field)

            if element is None:
                continue

            if element.text is None:
                continue

            value = element.text.strip()

            if value:
                metadata[library_field] = value

        games[filename] = metadata

    return games


def get_games(system_folder, system):
    """
    Obtiene los juegos reales de una carpeta de sistema
    respetando scan y extensions definidos en systems.json.
    """

    scan = system.get(
        "scan",
        "file"
    )

    if scan == "folder":

        return sorted(
            (
                item
                for item in system_folder.iterdir()
                if item.is_dir()
            ),
            key=lambda path: path.name.lower()
        )

    extensions = {
        extension.lower().lstrip(".")
        for extension in system.get(
            "extensions",
            []
        )
    }

    return sorted(
        (
            item
            for item in system_folder.iterdir()
            if (
                item.is_file()
                and item.suffix.lower().lstrip(".")
                in extensions
            )
        ),
        key=lambda path: path.name.lower()
    )


def create_game_entry(
    game_path,
    system,
    gamelist
):
    """
    Crea una entrada de games usando siempre
    el nombre real del juego en ROMs como clave.
    """

    if game_path.is_dir():

        game_name = game_path.name

        filename = game_path.name

    else:

        game_name = game_path.stem

        filename = game_path.name

    game = {
        "platform": system["name"],
        "developer": "",
        "publisher": "",
        "genre": "",
        "release": "",
        "players": "",
        "rating": "",
        "description": ""
    }

    xml_metadata = gamelist.get(
        filename,
        {}
    )

    for field in (
        "developer",
        "publisher",
        "genre",
        "release",
        "players",
        "rating",
        "description"
    ):

        if field in xml_metadata:

            game[field] = xml_metadata[field]

    return game_name, game


def generate_library(
    systems_file,
    roms_root,
    gamelists_root,
    output_file
):

    systems_data = load_json(
        systems_file
    )

    systems = systems_data.get(
        "systems",
        []
    )

    library_systems = []
    library_games = {}

    for system in systems:

        system_name = system["name"]

        system_folder = (
            roms_root / system_name
        )

        # El sistema solo pertenece a la biblioteca
        # si su carpeta existe.
        if not system_folder.is_dir():
            continue

        library_systems.append(
            system_name
        )

        gamelist_file = (
            gamelists_root
            / system_name
            / "gamelist.xml"
        )

        gamelist = load_gamelist(
            gamelist_file
        )

        games = get_games(
            system_folder,
            system
        )

        for game_path in games:

            game_name, game_data = create_game_entry(
                game_path,
                system,
                gamelist
            )

            library_games[game_name] = game_data

    library = {
        "systems": library_systems,
        "games": library_games
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            library,
            file,
            indent=2,
            ensure_ascii=False
        )

        file.write("\n")

    return library


def main():

    if len(sys.argv) != 5:

        print()
        print("Uso:")
        print()
        print(
            "python3 generate_library.py "
            "\"systems.json\" "
            "\"ROMs\" "
            "\"gamelists\" "
            "\"library.json\""
        )
        print()

        sys.exit(1)

    systems_file = Path(
        sys.argv[1]
    )

    roms_root = Path(
        sys.argv[2]
    )

    gamelists_root = Path(
        sys.argv[3]
    )

    output_file = Path(
        sys.argv[4]
    )

    if not systems_file.is_file():

        print(
            f"Error: no existe {systems_file}"
        )

        sys.exit(1)

    if not roms_root.is_dir():

        print(
            f"Error: no existe {roms_root}"
        )

        sys.exit(1)

    library = generate_library(
        systems_file,
        roms_root,
        gamelists_root,
        output_file
    )

    print()
    print("Library generada correctamente.")
    print()
    print(
        f"Sistemas: {len(library['systems'])}"
    )
    print(
        f"Juegos:   {len(library['games'])}"
    )
    print(
        f"Archivo:  {output_file}"
    )
    print()


if __name__ == "__main__":
    main()