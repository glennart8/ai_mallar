# Dimensionality Reduction

Visualisera högdimensionell data i 2D.

## Användning

```python
# PCA
pca = PCA(n_components=2)
data_2d = pca.fit_transform(data)

# t-SNE
tsne = TSNE(n_components=2)
data_2d = tsne.fit_transform(data)
```

## När använda

- Visualisera embeddings
- Förstå datastrukturer
- Hitta grupper/kluster visuellt
- Minska dimensioner innan ML

## PCA vs t-SNE

**PCA:**
- Snabb
- Bra för linjära relationer
- Bevarar global struktur
- Förklarad varians är tolkningsbar

**t-SNE:**
- Långsammare
- Bra för icke-linjära relationer
- Bevarar lokal struktur
- Bra för klustervisualisering

## Parametrar

PCA:
- `n_components` - Antal dimensioner att behålla

t-SNE:
- `perplexity` - Balans lokal/global (5-50, default 30)
- `n_iter` - Antal iterationer

## Tips

- Normalisera data först
- För stora dataset: använd PCA först, sedan t-SNE
- t-SNE är stokastisk - kör flera gånger
