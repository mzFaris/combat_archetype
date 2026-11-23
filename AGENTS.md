# AGENTS.md

Small uv/Python project that clusters Pokémon base stats into combat archetypes with scikit-learn, then plots the elbow, silhouette, and PCA scatter. There is no server, package split, or test suite.

## Setup and commands

- Use `uv` (already installed, 0.13.9). A `.venv/` exists and is managed by `uv`; do not hand-edit it.
- Run the analysis: `uv run combat-archetype` from the **repo root**. The script opens `pokemon.csv` by relative path, so any other working directory fails with `FileNotFoundError`.
- Equivalent direct run: `uv run python -c "from combat_archetype import main; main()"`.
- Headless/CI runs: `MPLBACKEND=Agg uv run combat-archetype`. Without a display, `plt.show()` emits "FigureCanvasAgg is non-interactive" warnings but still completes and prints the explained-variance line.
- There is no configured lint, format, typecheck, or test command, and no CI. Do not invent one; verify changes by running the analysis and reading its output.
- Python is pinned to `3.15` (`.python-version` and `requires-python = ">=3.15"`); the interpreter is already in `.venv`.

## Architecture and quirks

- Entire program lives in `src/combat_archetype/__init__.py`; `main()` is re-exported there and wired as the `combat-archetype` console script. Keep that entrypoint contract if you split code.
- `import plt` is intentional: the PyPI `plt` package is a one-line shim (`from matplotlib.pyplot import *`) that pulls in matplotlib. Do not "fix" it to `import matplotlib.pyplot as plt`; `matplotlib` is installed transitively via `plt`.
- Features are the six base stats only (`hp, attack, defense, sp_attack, sp_defense, speed`), standardized with `StandardScaler` before clustering.
- Number of clusters is hardcoded as `k = 5` after the elbow/silhouette plots. Changing the chosen `k` means editing that line; plots are diagnostic only and block waiting for a window when a display is available.
- `pokemon.csv` (801 data rows) is the only data source and is committed; schema changes require updating the `stat_cols` list.
- `README.md` is empty and the `pyproject.toml` description is a placeholder; do not treat them as documentation of intent.
