"""
Anomaly Detection - Hitta avvikelser i data.
Exempel: identifiera misstänkta transaktioner.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# Skapa exempeldata med några anomalier
np.random.seed(42)
normal_data = np.random.normal(loc=100, scale=15, size=(100, 2))
anomalies = np.array([[200, 200], [10, 10], [150, 20]])  # Tydliga outliers

data = pd.DataFrame(
    np.vstack([normal_data, anomalies]),
    columns=["transaction_amount", "time_seconds"]
)

print(f"Antal datapunkter: {len(data)}")

# Skapa och träna modell
model = IsolationForest(
    contamination=0.05,  # Förväntad andel anomalier (5%)
    random_state=42
)
model.fit(data)

# Gör prediktioner (-1 = anomali, 1 = normal)
predictions = model.predict(data)
data["is_anomaly"] = predictions == -1

# Anomali-score (lägre = mer avvikande)
data["score"] = model.score_samples(data[["transaction_amount", "time_seconds"]])

# Visa resultat
print(f"\nHittade {data['is_anomaly'].sum()} anomalier:")
print(data[data["is_anomaly"]][["transaction_amount", "time_seconds", "score"]])

# Kolla en ny transaktion
new_transaction = pd.DataFrame({
    "transaction_amount": [250],
    "time_seconds": [5]
})
is_anomaly = model.predict(new_transaction)[0] == -1
score = model.score_samples(new_transaction)[0]
print(f"\nNy transaktion:")
print(f"  Belopp: 250, Tid: 5 sek")
print(f"  Anomali: {'Ja' if is_anomaly else 'Nej'} (score: {score:.3f})")
