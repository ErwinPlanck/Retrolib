def main_menu():

    print()
    print("╔══════════════════════════════════════════╗")
    print("║                 RetroLib                 ║")
    print("╠══════════════════════════════════════════╣")
    print("║                                          ║")
    print("║  1. Verificar biblioteca                 ║")
    print("║  2. Configurar RetroArch                 ║")
    print("║  3. Exportar                             ║")
    print("║  4. Configurar Pegasus                   ║")
    print("║  5. Salir                                ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print()

    return input("Selecciona una opción: ").strip()


def export_menu():

    print()
    print("╔══════════════════════════════════════════╗")
    print("║                  Exportar                ║")
    print("╠══════════════════════════════════════════╣")
    print("║                                          ║")
    print("║  1. Exportar para RetroArch              ║")
    print("║  2. Exportar para Pegasus                ║")
    print("║  3. Volver                               ║")
    print("║                                          ║")
    print("╚══════════════════════════════════════════╝")
    print()

    return input("Selecciona una opción: ").strip()


def pause():

    input("\nPulsa ENTER para continuar...")


def print_results(results):

    if not results:
        print("No hay resultados para mostrar.")
        return

    current_section = None

    for result in results:

        section = result.get(
            "section",
            "Resultados"
        )

        if section != current_section:

            print()
            print(section)
            print("-" * len(section))

            current_section = section

        name = result.get(
            "name",
            "Desconocido"
        )

        exists = result.get(
            "exists",
            False
        )

        status = "✓" if exists else "✗"

        line = f"{status} {name}"

        if "roms" in result:
            line += f" ({result['roms']} juegos)"

        if "core" in result:
            line += f" — {result['core']}"

        print(line)

        if not exists:

            missing = result.get(
                "missing",
                []
            )

            for item in missing:
                print(f"    Falta: {item}")


def retroarch_not_found():

    print()
    print("RetroArch no fue encontrado.")
    print()
    print("  ENTER  →  Configurar las rutas manualmente")
    print("  r      →  Volver a buscar")
    print("  q      →  Salir")
    print()

    return input(
        "Selecciona una opción: "
    ).strip().lower()


def ask_retroarch_cfg_path():

    print()
    print("No se encontró el archivo de configuración de RetroArch.")
    print()
    print("Introduce la ruta al archivo:")
    print()
    print("  retroarch.cfg")
    print()
    print("Puedes arrastrar el archivo desde el explorador")
    print("de archivos a la terminal.")
    print()

    return input("Ruta: ").strip()


def ask_retroarch_executable_path():

    print()
    print("No se encontró el ejecutable de RetroArch.")
    print()
    print("Introduce la ruta al ejecutable:")
    print()
    print("  retroarch.exe")
    print()
    print("Puedes arrastrar el archivo desde el explorador")
    print("de archivos a la terminal.")
    print()

    return input("Ruta: ").strip()


def retroarch_options():

    print()
    print("La configuración de RetroArch necesita atención.")
    print()
    print("  ENTER  →  Corregir automáticamente")
    print("  r      →  Volver a verificar")
    print("  q      →  Cancelar")
    print()

    return input(
        "Selecciona una opción: "
    ).strip().lower()


def retry_options():

    print()
    print("La biblioteca no está completa.")
    print()
    print("  ENTER  →  Volver a verificar")
    print("  q      →  Salir")
    print()

    return input(
        "Selecciona una opción: "
    ).strip().lower()