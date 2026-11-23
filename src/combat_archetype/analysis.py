"""Clustering and dimensionality reduction for combat archetypes."""

import numpy as np
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from .data import STAT_COLUMNS

RANDOM_STATE = 42
K_MIN = 2
K_MAX = 10


def scale_stats(df: DataFrame) -> np.ndarray:
    return StandardScaler().fit_transform(df[STAT_COLUMNS])


def evaluate_k(
    X_scaled: np.ndarray,
    k_min: int = K_MIN,
    k_max: int = K_MAX,
) -> tuple[list[int], list[float], list[float]]:
    k_values = list(range(k_min, k_max + 1))
    inertia: list[float] = []
    silhouettes: list[float] = []

    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE)
        labels = kmeans.fit_predict(X_scaled)
        inertia.append(kmeans.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))

    return k_values, inertia, silhouettes


def fit_clusters(X_scaled: np.ndarray, k: int) -> np.ndarray:
    kmeans = KMeans(n_clusters=k, random_state=RANDOM_STATE)
    return kmeans.fit_predict(X_scaled)


def project_pca(X_scaled: np.ndarray) -> tuple[np.ndarray, PCA]:
    """Project the scaled stats onto two principal components."""
    pca = PCA(n_components=2)
    return pca.fit_transform(X_scaled), pca
