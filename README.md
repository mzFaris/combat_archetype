# Combat Archetype

Cluster Pokémon by their base stats to discover combat archetypes. The six base
stats are standardized, grouped with KMeans, and projected to 2D with PCA for
visualization.

## Setup

Requires [uv](https://docs.astral.sh/uv/). Python 3.15 is pinned in
`.python-version`; `uv` provisions it automatically.

```bash
uv sync
```

## Usage

Run from the repository root so the default `pokemon.csv` is found. There are
two mutually exclusive modes:

```bash
# Explore k = 2..10: prints an inertia/silhouette table and shows the
# elbow and silhouette plots, then exits.
uv run combat-archetype --diagnose

# Fit the final model with k = 5: shows the PCA scatter and prints the
# explained variance.
uv run combat-archetype --k 5
```

| Option | Description |
| --- | --- |
| `-k, --k N` | Number of clusters for the final model. Must be at least 2. |
| `--diagnose` | Run the k diagnostics only; no final model or scatter plot. |
| `-i, --input PATH` | CSV to analyze (default: `pokemon.csv`). |

`--k` and `--diagnose` are mutually exclusive, and one of them is required.

```bash
uv run combat-archetype --k 3 --input path/to/pokemon.csv
```

In a headless environment, disable interactive windows:

```bash
MPLBACKEND=Agg uv run combat-archetype --diagnose
```

## How it works

1. Load `pokemon.csv` and select the six base stats: `hp`, `attack`, `defense`,
   `sp_attack`, `sp_defense`, `speed`.
2. Standardize the stats with `StandardScaler`.
3. In `--diagnose` mode, run KMeans for `k = 2..10`, reporting inertia and
   silhouette scores to help choose a cluster count.
4. In `--k` mode, fit KMeans with the chosen `k`, project the data to two
   principal components, color the scatter plot by cluster, and print how much
   variance PC1 and PC2 explain.

## Project layout

```
src/combat_archetype/
  cli.py       # argparse modes and orchestration
  data.py      # STAT_COLUMNS and CSV loading
  analysis.py  # scaling, KMeans diagnostics, final clusters, PCA
  plotting.py  # elbow/silhouette and PCA scatter figures
```

The dataset (`pokemon.csv`) has 801 rows and is the only required input. If its
schema changes, update `STAT_COLUMNS` in `data.py`.
