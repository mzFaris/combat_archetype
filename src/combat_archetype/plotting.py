"""Plotting helpers.

`plt` is the PyPI shim over ``matplotlib.pyplot`` (``from matplotlib.pyplot
import *``), kept from the original script so plotting works as before.
"""

import numpy as np
import plt
from sklearn.decomposition import PCA


def plot_diagnostics(
    k_values: list[int],
    inertia: list[float],
    silhouettes: list[float],
) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(k_values, inertia, marker="o")
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("Inertia")
    axes[0].set_title("Elbow Method")

    axes[1].plot(k_values, silhouettes, marker="o", color="orange")
    axes[1].set_xlabel("k")
    axes[1].set_ylabel("Silhouette Score")
    axes[1].set_title("Silhouette Score")

    plt.tight_layout()
    plt.show()


def plot_clusters(X_2d: np.ndarray, labels: np.ndarray, pca: PCA, k: int) -> None:
    """Show the PCA projection colored by cluster assignment."""
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        X_2d[:, 0], X_2d[:, 1], c=labels, cmap="tab10", alpha=0.6, s=30
    )
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    plt.title(f"Pokémon Combat Archetypes (k={k})")
    plt.colorbar(scatter, label="Cluster")
    plt.show()
