# Clustering

Gruppera liknande objekt automatiskt utan fördefinierade klasser.

## Användning

```python
# Normalisera data
scaler = StandardScaler()
data_normalized = scaler.fit_transform(data)

# Klustra
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(data_normalized)
```

## När använda

- Kundsegmentering
- Gruppera dokument/artiklar
- Marknadsanalys
- Bildsegmentering
- Identifiera mönster i data

## Välja antal kluster

Elbow-metoden:
1. Kör KMeans med k=1,2,3...
2. Plotta inertia
3. Välj k där kurvan "knäcker" (armbågen)

## Alternativa algoritmer

```python
from sklearn.cluster import DBSCAN      # Hanterar godtyckliga former
from sklearn.cluster import AgglomerativeClustering  # Hierarkisk
```

## Viktiga delar

- **StandardScaler** - Normalisera data (annars dominerar stora värden)
- **inertia_** - Mått på hur täta klustren är
- **predict()** - Tilldela nya datapunkter till kluster

## Tips

- Normalisera alltid data först
- Prova olika antal kluster
- Visualisera resultaten om möjligt
