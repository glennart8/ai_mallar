# Anomaly Detection

Hitta avvikelser och outliers i data.

## Användning

```python
model = IsolationForest(contamination=0.05)
model.fit(data)

# -1 = anomali, 1 = normal
predictions = model.predict(data)
```

## När använda

- Bedrägeridetektion (fraud detection)
- Upptäcka fel i maskiner/sensorer
- Identifiera ovanliga kundbeteenden
- Kvalitetskontroll i produktion
- Nätverksintrångsdetektering

## Alternativa modeller

```python
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
```

## Parametrar

- `contamination` - Förväntad andel anomalier (0.01-0.5)
- Lägre = färre anomalier hittas
- Högre = fler anomalier hittas (risk för falska positiva)

## Resultat

- `predict()` returnerar -1 (anomali) eller 1 (normal)
- `score_samples()` ger kontinuerlig score (lägre = mer avvikande)
- Använd score för att ranka misstänkta fall
