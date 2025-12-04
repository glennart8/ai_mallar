"""
Dimensionality Reduction - Visualisera högdimensionell data.
Reducera många dimensioner till 2D för visualisering.
"""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Skapa exempeldata (hög dimension)
np.random.seed(42)
n_samples = 150

# Tre grupper i 10 dimensioner
group1 = np.random.normal(0, 1, (50, 10))
group2 = np.random.normal(3, 1, (50, 10))
group3 = np.random.normal(6, 1, (50, 10))

data = np.vstack([group1, group2, group3])
labels = [0]*50 + [1]*50 + [2]*50

print(f"Original data: {data.shape[0]} samples, {data.shape[1]} dimensioner")

# Normalisera
scaler = StandardScaler()
data_norm = scaler.fit_transform(data)

# PCA - snabb, bra för linjära relationer
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data_norm)

print(f"\nPCA - Förklarad varians: {pca.explained_variance_ratio_.sum():.1%}")
print(f"  Komponent 1: {pca.explained_variance_ratio_[0]:.1%}")
print(f"  Komponent 2: {pca.explained_variance_ratio_[1]:.1%}")

# t-SNE - bra för icke-linjära relationer
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
data_tsne = tsne.fit_transform(data_norm)

# Visualisera
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# PCA plot
scatter1 = axes[0].scatter(data_pca[:, 0], data_pca[:, 1], c=labels, cmap="viridis")
axes[0].set_title("PCA")
axes[0].set_xlabel("PC1")
axes[0].set_ylabel("PC2")

# t-SNE plot
scatter2 = axes[1].scatter(data_tsne[:, 0], data_tsne[:, 1], c=labels, cmap="viridis")
axes[1].set_title("t-SNE")
axes[1].set_xlabel("Dim 1")
axes[1].set_ylabel("Dim 2")

plt.tight_layout()
plt.savefig("dimensionality_reduction.png", dpi=100)
print("\nVisualisering sparad som 'dimensionality_reduction.png'")
