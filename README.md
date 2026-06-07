# Death Counter

A simple desktop application for tracking deaths in roguelike games. Because every death is a lesson — and you need to know how many lessons you've had.

Built with Python and tkinter. The counter is incremented manually — no automation, no integration, just a button you click when you die.

## Features

- **Multiple games** — add as many games as you want, each with its own death counter
- **Persistent storage** — data is saved to your OS application data directory (`%APPDATA%/death-counter/` on Windows, `~/.local/share/death-counter/` on Linux)
- **Manual +1** — click a button, die one more time
- **Set any value** — need to correct the count? Set it to whatever number you want
- **Portable executable** — no Python installation required for the pre-built binary

## Screenshot

```
┌──────────────────────────────────────┐
│  Death Counter                       │
├───────────┬──────────────────────────┤
│  Games    │ Nethack                  │
│  ┌─────┐  │                          │
│  │Rogue│  │          ┌─────┐         │
│  │Neth.│  │          │ 147 │         │
│  │DCSS │  │          └─────┘         │
│  └─────┘  │                          │
│ [+Add]    │  [ +1 Death ]            │
│ [Remove]  │  [ Set Value ]           │
└───────────┴──────────────────────────┘
```

## Usage

1. Launch the application
2. Click **+ Add Game** to create a new game entry
3. Select a game from the list
4. Click **+1 Death** every time you die
5. Use **Set Value** if you need to adjust the number manually
6. Close the window — your data is saved automatically

All data persists between sessions. You can delete the executable and re-download it — your counters are safe in the app data directory.

## Download

Pre-built binaries are available from the [Releases](https://github.com/yourusername/death-counter/releases) page:

| Platform | File                                    |
|----------|-----------------------------------------|
| Windows  | `Death Counter.exe`                     |
| Linux    | `Death Counter` (requires `python3-tk`) |

No Python or any runtime is needed on Windows — just download and run.

## Build from Source

### Prerequisites

- Python 3.9+

### Build

```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "Death Counter" death_counter.py
```

The executable will be at `dist/Death Counter.exe` (Windows) or `dist/Death Counter` (Linux).

### Run without building

```bash
python death_counter.py
```

No third-party Python packages are required — the app uses only the standard library.

## CI / Automated Builds

This repository includes a GitHub Actions workflow (`.github/workflows/build.yml`) that:

- Builds Windows and Linux binaries on every push
- Uploads them as build artifacts
- Creates a GitHub Release with attached binaries when a tag matching `v*` is pushed

To trigger a release:

```bash
git tag v1.0
git push origin v1.0
```

Then go to the repository's Releases page to download.

## Data Storage

| OS      | Path                                       |
|---------|--------------------------------------------|
| Windows | `%APPDATA%\death-counter\deaths.json`      |
| Linux   | `~/.local/share/death-counter/deaths.json` |

To back up or restore your data, copy this file. Deleting or moving the executable has no effect on saved data.

## License

MIT
