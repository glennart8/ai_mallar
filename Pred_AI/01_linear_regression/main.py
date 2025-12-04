"""
Linear Regression - Förutsäga numeriska värden.
Exempel: förutsäga pris baserat på storlek.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Skapa exempeldata (ersätt med din egen data)
data = pd.DataFrame({
    "size_sqm": [50, 65, 80, 95, 110, 125, 140, 155, 170, 185],
    "rooms": [1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
    "price_tkr": [1500, 2000, 2400, 2900, 3300, 3800, 4200, 4700, 5100, 5600]
})

# Separera features (X) och target (y)
X = data[["size_sqm", "rooms"]]
y = data["price_tkr"]

# Dela upp i träning och test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Skapa och träna modell
model = LinearRegression()
model.fit(X_train, y_train)

# Gör prediktioner
y_pred = model.predict(X_test)

# Utvärdera modellen
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")
print(f"\nKoefficienter: {dict(zip(X.columns, model.coef_))}")
print(f"Intercept: {model.intercept_:.2f}")

# Göra en ny prediktion
new_apartment = pd.DataFrame({"size_sqm": [100], "rooms": [3]})
prediction = model.predict(new_apartment)
print(f"\nPrediktion för 100 kvm, 3 rum: {prediction[0]:.0f} tkr")
