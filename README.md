# RetroLib

RetroLib is a lightweight game-library manager designed to organize ROMs and configure RetroArch and Pegasus Frontend from a single directory structure.

The project is designed around a simple idea:

> Put your games in the expected folders, let RetroLib verify the environment, and generate the configuration files required by your frontends.

RetroLib currently targets macOS and Windows, while keeping platform-specific behavior isolated from the rest of the application.

---

## Features

- Automatic detection of supported systems from the ROM directory structure.
- Centralized system definitions through `systems.json`.
- Automatic generation of `library.json`.
- Game metadata extraction from `gamelist.xml`.
- Exact-name matching between ROMs and XML metadata.
- RetroArch configuration verification and repair.
- Core verification.
- BIOS verification.
- Automatic Asset directory creation.
- RetroArch playlist generation.
- Pegasus metadata generation.
- Pegasus game-directory configuration.
- Cross-platform core filename handling:
  - macOS → `.dylib`
  - Windows → `.dll`
  - Linux → `.so`
- Platform-specific handling for RetroArch and Pegasus.
- Clean game names for frontend display.

---

## Directory Structure

A typical installation looks like this:

```text
RetroLib/
├── RetroLib.command
│
├── ROMs/
├── BIOS/
├── Cores/
├── CoreInfo/
├── Assets/
├── Metadata/
├── Thumbnails/
├── Saves/
├── SaveStates/
│
└── Tools/
    ├── data/
    │   ├── config.json
    │   ├── systems.json
    │   └── library.json
    │
    └── scripts/
        ├── exports/
        ├── platforms/
        ├── assets.py
        ├── bios.py
        ├── config.py
        ├── cores.py
        ├── display.py
        ├── generate_library.py
        ├── get_files.py
        ├── library.py
        ├── pegasus_config.py
        ├── retroarch_config.py
        ├── retrolib.py
        └── verify.py
```

| Directory | Purpose |
|---|---|
| `ROMs` | Game files |
| `BIOS` | BIOS files required by systems |
| `Cores` | RetroArch cores |
| `CoreInfo` | RetroArch core information |
| `Assets` | Game artwork and media |
| `Metadata` | Generated RetroArch and Pegasus metadata |
| `Thumbnails` | RetroArch thumbnails |
| `Saves` | Save files |
| `SaveStates` | Save states |

`Tools` contains RetroLib itself and its internal data.

---

## Systems

RetroLib uses `systems.json` as the master catalog of supported systems.

A system definition contains information such as:

```json
{
  "name": "Nintendo - Entertainment System",
  "core": "Mesen",
  "core_name": "Nintendo - NES / Famicom (Mesen)",
  "core_library": "mesen_libretro",
  "playlist": "Nintendo - Nintendo Entertainment System",
  "extensions": [
    "nes",
    "fds",
    "unf",
    "unif"
  ],
  "scan": "file"
}
```

The catalog defines the systems RetroLib knows how to handle.

The presence of a system in `systems.json` does not mean that the system must exist in the user's installation.

RetroLib determines which systems are actually being used from the contents of `ROMs`.

For example:

```text
ROMs/
├── Nintendo - Entertainment System/
├── Nintendo - Super Nintendo Entertainment System/
└── Sony - PlayStation/
```

Only those systems are included in the generated `library.json`.

This allows `systems.json` to act as the master catalog while `library.json` represents the user's actual library.

---

## Library Generation

`library.json` is generated automatically from:

- `systems.json`
- the contents of `ROMs`
- available `gamelist.xml` metadata

The generated library contains the systems currently present in the user's ROM directory and the games found inside them.

Game metadata can include:

```json
{
  "Super Metroid": {
    "platform": "Super Nintendo Entertainment System",
    "developer": "Nintendo",
    "publisher": "Nintendo",
    "genre": "Platform",
    "release": "1994",
    "players": "1",
    "description": "..."
  }
}
```

Metadata is matched using the exact game name.

If the name in the ROM library and the name in the XML do not match, the entries are ignored rather than guessed or automatically renamed.

This is intentional: RetroLib prioritizes predictable and deterministic metadata matching.

---

## Verification

Before generating frontend files, RetroLib verifies the current installation.

The verification process includes:

- Library structure and ROM files.
- Required RetroArch cores.
- BIOS requirements defined by each system.
- RetroArch directory configuration.

If a RetroArch directory is incorrectly configured, RetroLib reports the problem and can repair the configuration.

---

## RetroArch

RetroLib can generate RetroArch playlists automatically.

Generated playlists are stored in:

```text
Metadata/
└── RetroArch/
```

Each playlist contains:

- Game paths.
- Game labels.
- Core paths.
- Core names.
- Playlist database information.

Core filenames are resolved according to the operating system:

```text
macOS
sameboy_libretro.dylib

Windows
sameboy_libretro.dll

Linux
sameboy_libretro.so
```

This allows `systems.json` to remain independent of the operating system.

---

## Pegasus Frontend

RetroLib can also generate metadata for Pegasus Frontend.

Generated metadata is stored in:

```text
Metadata/
└── Pegasus/
    └── <System>/
        └── metadata.pegasus.txt
```

The generated metadata includes:

- Collection information.
- Game names.
- ROM paths.
- Artwork paths.
- Video paths.
- Developer.
- Publisher.
- Genre.
- Release date.
- Player count.
- Description.
- Platform.

RetroLib also configures the Pegasus `game_dirs.txt` file so Pegasus can locate the generated collections.

---

## Game Names

ROM filenames may contain information that is useful for identification but undesirable for frontend display.

For example:

```text
Super Metroid (Japan, USA) (En,Ja)
```

is displayed as:

```text
Super Metroid
```

The original filename is still used internally to locate the game and match metadata.

Only the frontend display name is cleaned.

This keeps file identification separate from presentation.

---

## Platform Support

RetroLib isolates operating-system-specific functionality inside:

```text
Tools/scripts/platforms/
```

Current platform modules include:

```text
platforms/
├── __init__.py
├── macos.py
└── windows.py
```

Platform-specific functionality includes:

- RetroArch core extensions.
- RetroArch configuration locations.
- RetroArch executable locations.
- Pegasus configuration locations.

Current core extensions are:

| Platform | Extension |
|---|---|
| macOS | `.dylib` |
| Windows | `.dll` |
| Linux | `.so` |

---

## Running RetroLib

RetroLib can be executed directly from the terminal.

From:

```text
RetroLib/Tools/scripts/
```

run:

```bash
python3 retrolib.py
```

On macOS, a launcher can also be provided in the root directory:

```text
RetroLib.command
```

This allows RetroLib to be started by double-clicking the launcher from Finder while still running it through the terminal.

---

## Configuration

RetroLib stores its internal configuration in:

```text
Tools/data/config.json
```

The configuration can store information such as the location of the RetroArch configuration file.

If RetroArch cannot be detected automatically, RetroLib can ask the user for its location.

The same approach allows RetroLib to work with installations that use non-standard paths.

---

## Design Philosophy

RetroLib is intentionally built around a few principles.

### Predictability

RetroLib should not silently guess what a game or system is.

If names do not match, they are ignored.

### Centralized definitions

Systems are defined once in `systems.json`.

The generated `library.json` only contains the systems and games actually present in the user's installation.

### Platform independence

Platform-specific paths and filenames are isolated inside `platforms/`.

The rest of RetroLib should not need operating-system-specific logic.

### Separation of responsibilities

RetroLib separates:

```text
System definitions
        ↓
Library generation
        ↓
Verification
        ↓
Frontend export
```

RetroArch and Pegasus are treated as exporters rather than as the source of truth for the library.

---

## Current Exporters

RetroLib currently supports:

```text
RetroArch
Pegasus Frontend
```

Both exporters operate from the same generated library.

This means the ROM collection and metadata do not need to be maintained independently for each frontend.

---

## Roadmap

Planned or possible future functionality includes:

- Windows-specific testing.
- Steam library integration.
- Additional frontend exporters.
- Additional metadata sources.
- Improved installation and distribution.
- Additional supported systems.
- More automated environment detection.

Steam integration is intentionally kept separate from the current RetroArch workflow. The goal is to support Steam games without turning RetroLib into a general-purpose executable scanner.

---

## Project Status

RetroLib is currently functional on macOS and has a cross-platform architecture prepared for Windows.

The current system is capable of:

```text
ROMs
 ↓
System detection
 ↓
Library generation
 ↓
Verification
 ↓
RetroArch export
 ↓
Pegasus export
```

with platform-specific paths and core filenames handled automatically.

---

## License
