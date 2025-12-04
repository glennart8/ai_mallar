"""
Classification - Kategorisera data i klasser.
Exempel: klassificera kunder som churnade eller ej.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Skapa exempeldata (ersätt med din egen data)
data = pd.DataFrame({
    "age": [25, 45, 35, 50, 23, 40, 60, 48, 33, 55],
    "months_customer": [1, 24, 12, 36, 2, 18, 48, 30, 6, 42], # antal månader som kund
    "support_tickets": [5, 1, 2, 0, 8, 1, 0, 2, 6, 1], # antal supportärenden
    "churned": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0]  # 1 = slutat vara kund, 0 = aktiv
})

# Separera features (X) och target (y)
X = data[["age", "months_customer", "support_tickets"]]
y = data["churned"]

# Dela upp i träning och test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Skapa och träna modell
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Gör prediktioner
y_pred = model.predict(X_test)

# Utvärdera modellen
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Aktiv", "Churnad"]))

# Feature importance
importance = dict(zip(X.columns, model.feature_importances_))
print(f"\nFeature Importance:")
for feature, imp in sorted(importance.items(), key=lambda x: x[1], reverse=True):
    print(f"  {feature}: {imp:.3f}")

# Göra en ny prediktion
new_customer = pd.DataFrame({
    "age": [30],
    "months_customer": [3],
    "support_tickets": [4]
})
prediction = model.predict(new_customer)
probability = model.predict_proba(new_customer)
print(f"\nNy kund - Prediktion: {'Churnad' if prediction[0] else 'Aktiv'}")
print(f"Sannolikhet: {probability[0][1]:.1%} risk för churn")
