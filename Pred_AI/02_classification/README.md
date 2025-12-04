# Classification

Kategorisera data i två eller flera klasser.

## Användning

```python
# Träna modell
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Klassificera
prediction = model.predict(new_data)
probability = model.predict_proba(new_data)
```

## När använda

- Spam vs icke-spam
- Churn-prediktion (lämnar kunden?)
- Kategorisera supportärenden
- Kreditriskbedömning
- Produktrekommendationer

## Alternativa modeller

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
```

## Utvärdering

- **Accuracy** - Andel korrekta prediktioner
- **Precision** - Av de vi sa "positiv", hur många var rätt?
- **Recall** - Av de faktiska positiva, hur många hittade vi?
- **F1-Score** - Balans mellan precision och recall

## Feature Importance

RandomForest ger feature_importances_ som visar vilka
variabler som är viktigast för prediktionen.
