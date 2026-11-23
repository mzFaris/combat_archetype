"""Command-line entrypoint for the combat archetype analysis."""

import argparse

from .analysis import evaluate_k, fit_clusters, project_pca, scale_stats
from .data import load_pokemon
from .plotting import plot_clusters, plot_diagnostics


def _positive_k(value: str) -> int:
    try:
        k = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"k must be an integer, got {value!r}"
        ) from None
    if k < 2:
        raise argparse.ArgumentTypeError("k must be at least 2")
    return k


def _print_diagnostic_summary(
    k_values: list[int],
    inertia: list[float],
    silhouettes: list[float],
) -> None:
    print(f"{'k':>3}  {'inertia':>12}  {'silhouette':>10}")
    for k, value, score in zip(k_values, inertia, silhouettes):
        print(f"{k:>3}  {value:>12.3f}  {score:>10.3f}")

    best = max(range(len(silhouettes)), key=silhouettes.__getitem__)
    print(f"Best silhouette: k={k_values[best]} ({silhouettes[best]:.3f})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cluster Pokémon base stats into combat archetypes."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="pokemon.csv",
        help="path to the Pokémon CSV (default: %(default)s)",
    )

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "-k",
        "--k",
        type=_positive_k,
        help="number of clusters for the final model",
    )
    mode.add_argument(
        "--diagnose",
        action="store_true",
        help="show elbow/silhouette diagnostics only, then exit",
    )
    args = parser.parse_args()

    df = load_pokemon(args.input)
    X_scaled = scale_stats(df)

    if args.diagnose:
        k_values, inertia, silhouettes = evaluate_k(X_scaled)
        _print_diagnostic_summary(k_values, inertia, silhouettes)
        plot_diagnostics(k_values, inertia, silhouettes)
        return

    labels = fit_clusters(X_scaled, args.k)
    X_2d, pca = project_pca(X_scaled)
    plot_clusters(X_2d, labels, pca, args.k)

    print(f"PC1 + PC2 explain {pca.explained_variance_ratio_.sum():.1%} of variance")
