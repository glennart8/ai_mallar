"""
Clustering - Gruppera liknande objekt automatiskt.
Exempel: segmentera kunder baserat på beteende.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Skapa exempeldata (ersätt med din egen data)
np.random.seed(42)
data = pd.DataFrame({
    "purchases_per_month": np.concatenate([
        np.random.normal(2, 1, 30),    # Lågaktiva     Medelvärde, standardavvikelse, antal kunder
        np.random.normal(10, 2, 30),   # Medelaktiva
        np.random.normal(25, 3, 30)    # Högaktiva
    ]),
    "avg_order_value": np.concatenate([
        np.random.normal(100, 20, 30),  # Lågvärde
        np.random.normal(300, 50, 30),  # Medelvärde
        np.random.normal(800, 100, 30)  # Högvärde
    ])
})

print(f"Data: {len(data)} kunder")

# Normalisera data (viktigt för KMeans)
scaler = StandardScaler()
data_normalized = scaler.fit_transform(data)

# Hitta optimalt antal kluster (Elbow method)
inertias = []
for k in range(1, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(data_normalized)
    inertias.append(kmeans.inertia_)

print("\nInertia per antal kluster (leta efter 'armbågen'):")
for k, inertia in enumerate(inertias, 1):
    print(f"  k={k}: {inertia:.0f}")

# Klustra med valt antal (3 i detta fall)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
data["cluster"] = kmeans.fit_predict(data_normalized)

# Analysera klustren
print("\nKluster-statistik:")
for cluster in range(3):
    cluster_data = data[data["cluster"] == cluster]
    print(f"\nKluster {cluster} ({len(cluster_data)} kunder):")
    print(f"  Köp/månad: {cluster_data['purchases_per_month'].mean():.1f}")
    print(f"  Snitt ordervärde: {cluster_data['avg_order_value'].mean():.0f} kr")

# Klassificera en ny kund
new_customer = pd.DataFrame({
    "purchases_per_month": [15],
    "avg_order_value": [400]
})
new_customer_norm = scaler.transform(new_customer)
cluster = kmeans.predict(new_customer_norm)[0]
print(f"\nNy kund tillhör kluster: {cluster}")

# Visualisering
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Elbow-metoden
axes[0].plot(range(1, 8), inertias, "bo-")
axes[0].set_xlabel("Antal kluster (k)")
axes[0].set_ylabel("Inertia")
axes[0].set_title("Elbow-metoden - Hitta optimalt k")
axes[0].axvline(x=3, color="r", linestyle="--", label="Valt k=3")
axes[0].legend()

# Plot 2: Klustren visualiserade
colors = ["red", "green", "blue"]
for i in range(3):
    cluster_data = data[data["cluster"] == i]
    axes[1].scatter(
        cluster_data["purchases_per_month"],
        cluster_data["avg_order_value"],
        c=colors[i],
        label=f"Kluster {i}",
        alpha=0.6
    )

# Markera centroids
centroids = scaler.inverse_transform(kmeans.cluster_centers_)
axes[1].scatter(centroids[:, 0], centroids[:, 1], c="black", marker="X", s=200, label="Centroids")

axes[1].set_xlabel("Köp per månad")
axes[1].set_ylabel("Snitt ordervärde (kr)")
axes[1].set_title("Kundsegment")
axes[1].legend()

plt.tight_layout()
plt.show()
