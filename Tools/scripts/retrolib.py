from exports.retroarch import generate_playlists
from exports.pegasus import generate_metadata

from pegasus_config import configure_pegasus

from config import load_config, find_retroarch

from retroarch_config import (
    configure_retroarch,
    save_retroarch,
    load_retroarch,
    verify_retroarch
)

from library import load_library
from verify import verify_library
from cores import verify_cores
from bios import verify_bios
from assets import create_asset_directories

from display import (
    main_menu,
    export_menu,
    pause,
    print_results,
    retroarch_not_found,
    ask_retroarch_path,
    retroarch_options
)


def all_ok(results):
    return all(
        result["exists"]
        for result in results
    )


def create_assets(library, folders):

    for system in library["systems"]:

        create_asset_directories(
            system,
            folders
        )


def verify_library_system(library, folders):

    results = []

    results.extend(
        verify_library(
            library,
            folders
        )
    )

    results.extend(
        verify_cores(
            library,
            folders
        )
    )

    results.extend(
        verify_bios(
            library,
            folders
        )
    )

    print()
    print_results(results)

    print()

    if all_ok(results):
        print("La biblioteca está correctamente configurada.")
    else:
        print("Hay elementos que necesitan atención.")

    pause()


def configure_retroarch_system(
    retroarch_cfg,
    folders
):

    retroarch = load_retroarch(
        retroarch_cfg
    )

    results = verify_retroarch(
        retroarch,
        folders
    )

    print()
    print_results(results)

    if all_ok(results):

        print()
        print("RetroArch ya está correctamente configurado.")

        pause()

        return

    option = retroarch_options()

    if option == "q":
        return

    if option == "r":
        return

    retroarch = configure_retroarch(
        retroarch,
        folders
    )

    save_retroarch(
        retroarch
    )

    print()
    print("Configuración de RetroArch actualizada.")

    pause()


def export_retroarch(library, folders):

    print()
    print("Exportando para RetroArch...")
    print()

    generate_playlists(
        library,
        folders
    )

    print(
        "✓ Playlists de RetroArch generadas correctamente."
    )

    pause()


def export_pegasus(library, folders):

    print()
    print("Exportando para Pegasus...")
    print()

    generate_metadata(
        library,
        folders
    )

    print(
        "✓ Metadata de Pegasus generada correctamente."
    )

    pause()


def configure_pegasus_system(library, folders):

    pegasus_directories = get_pegasus_directories(
        library,
        folders
    )

    configure_pegasus(
        pegasus_directories
    )

    print()
    print("Pegasus configurado correctamente.")

    pause()


def get_pegasus_directories(library, folders):

    directories = []

    for system in library["systems"]:

        system_metadata_folder = (
            folders["metadata"]
            / "Pegasus"
            / system["name"]
        )

        if system_metadata_folder.exists():

            directories.append(
                system_metadata_folder
            )

    return directories


def find_retroarch_interactive(config):

    retroarch_cfg = find_retroarch(
        config
    )

    while retroarch_cfg is None:

        option = retroarch_not_found()

        if option == "q":
            return None

        if option == "r":

            retroarch_cfg = find_retroarch(
                config
            )

            continue

        path = ask_retroarch_path()

        retroarch_cfg = find_retroarch(
            config,
            path
        )

    return retroarch_cfg


def export_menu_loop(library, folders):

    while True:

        option = export_menu()

        if option == "1":

            export_retroarch(
                library,
                folders
            )

        elif option == "2":

            export_pegasus(
                library,
                folders
            )

        elif option == "3":
            return

        else:

            print()
            print("Opción no válida.")

            pause()


def main():

    config = load_config()

    retroarch_cfg = find_retroarch_interactive(
        config
    )

    if retroarch_cfg is None:
        return

    library, folders = load_library()

    create_assets(
        library,
        folders
    )

    while True:

        option = main_menu()

        if option == "1":

            verify_library_system(
                library,
                folders
            )

        elif option == "2":

            configure_retroarch_system(
                retroarch_cfg,
                folders
            )

        elif option == "3":

            export_menu_loop(
                library,
                folders
            )

        elif option == "4":

            configure_pegasus_system(
                library,
                folders
            )

        elif option == "5":

            print()
            print("Saliendo de RetroLib.")
            print()

            break

        else:

            print()
            print("Opción no válida.")

            pause()


if __name__ == "__main__":
    main()