# AGENTS.md

Small uv/Python project that clusters Pokémon base stats into combat archetypes with scikit-learn, then plots the elbow, silhouette, and PCA scatter. There is no server or test suite.

## Setup and commands

- Use `uv` (already installed, 0.13.9). A `.venv/` exists and is managed by `uv`; do not hand-edit it.
- Run from the **repo root**; one mode flag is required and the two are mutually exclusive:
  - `uv run combat-archetype --k 5` — fit the final model, show the PCA scatter, print explained variance.
  - `uv run combat-archetype --diagnose` — print a k/inertia/silhouette table, show the elbow/silhouette plots, then exit without fitting a final model.
- `-i/--input PATH` overrides the default `pokemon.csv`, resolved relative to the working directory; default-path runs from another directory fail with `FileNotFoundError`.
- `--k` values below `2` are rejected. Diagnostics always sweep `k = 2..10`, independent of the chosen `--k`.
- Equivalent direct run: `uv run python -c "from combat_archetype import main; main()"` (it will parse the process arguments, so pass `--diagnose` or `--k N`).
- Headless/CI runs: `MPLBACKEND=Agg uv run combat-archetype --diagnose` (or `--k N`). Without a display, `plt.show()` emits "FigureCanvasAgg is non-interactive" warnings but still completes: diagnose prints the table, `--k` prints the explained-variance line.
- There is no configured lint, format, typecheck, or test command, and no CI. Do not invent one; verify changes by running the analysis and reading its output.
- Python is pinned to `3.15` (`.python-version` and `requires-python = ">=3.15"`); the interpreter is already in `.venv`.

## Architecture and quirks

- `src/combat_archetype/`: `cli.py` (argparse and orchestration, defines `main`), `data.py` (`STAT_COLUMNS`, `load_pokemon`), `analysis.py` (scaling, k diagnostics, KMeans, PCA), `plotting.py` (diagnostic and scatter figures). `__init__.py` re-exports `main`, which is wired as the `combat-archetype` console script; keep that entrypoint contract.
- `import plt` is intentional: the PyPI `plt` package is a one-line shim (`from matplotlib.pyplot import *`) that pulls in matplotlib. Do not "fix" it to `import matplotlib.pyplot as plt`; `matplotlib` is installed transitively via `plt`.
- Features are the six base stats only (`hp, attack, defense, sp_attack, sp_defense, speed`), standardized with `StandardScaler` before clustering.
- `RANDOM_STATE = 42` lives in `analysis.py` and is shared by the diagnostic and final KMeans models; changing it changes the clusters.
- `pokemon.csv` (801 data rows) is the only data source and is committed; schema changes require updating `STAT_COLUMNS` in `data.py`.
- `README.md` is empty and the `pyproject.toml` description is a placeholder; do not treat them as documentation of intent.
