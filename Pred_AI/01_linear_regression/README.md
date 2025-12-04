# Linear Regression

Förutsäga numeriska värden baserat på input-variabler.

## Användning

```python
# Träna modell
model = LinearRegression()
model.fit(X_train, y_train)

# Förutsäg
prediction = model.predict(new_data)
```

## När använda

- Förutsäga priser (bostäder, produkter)
- Estimera försäljning baserat på marknadsföringsbudget
- Prognostisera kostnader
- Bestämma samband mellan variabler

## Steg

1. Förbered data (features X, target y)
2. Dela upp i träning/test
3. Träna modellen med fit()
4. Utvärdera med MSE och R2
5. Gör prediktioner med predict()

## Utvärdering

- **MSE** (Mean Squared Error) - Lägre är bättre
- **R2 Score** - Nära 1.0 är bättre (förklarar variansen)
- **Koefficienter** - Visar påverkan av varje feature
