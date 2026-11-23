from sklearn.decomposition import PCA
import plt
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pandas import read_csv

def main() -> None:
    df = read_csv("pokemon.csv")
    stat_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]

    X = df[stat_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    inertia = []
    silhouettes = []
    K_range = range(2, 11)

    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        inertia.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, labels))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(K_range, inertia, marker="o")
    axes[0].set_xlabel("k")
    axes[0].set_ylabel("Inertia")
    axes[0].set_title("Elbow Method")

    axes[1].plot(K_range, silhouettes, marker="o", color="orange")
    axes[1].set_xlabel("k")
    axes[1].set_ylabel("Silhouette Score")
    axes[1].set_title("Silhouette Score")

    plt.tight_layout()
    plt.show()

    k = 5  # replace with your chosen k
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    # PCA to 2D for visualization
    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_scaled)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_2d[:, 0], X_2d[:, 1], c=df["cluster"], cmap="tab10", alpha=0.6, s=30)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    plt.title(f"Pokémon Combat Archetypes (k={k})")
    plt.colorbar(scatter, label="Cluster")
    plt.show()

    print(f"PC1 + PC2 explain {pca.explained_variance_ratio_.sum():.1%} of variance")
