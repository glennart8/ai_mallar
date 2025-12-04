"""
Time Series Forecasting - Prognostisera framtida värden.
Exempel: förutsäga försäljning för kommande månader.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Skapa exempeldata (ersätt med din egen data)
# Månadsdata för försäljning
dates = pd.date_range(start="2023-01-01", periods=24, freq="M")
sales = [100, 120, 130, 125, 140, 160, 180, 175, 190, 210, 200, 220,
         230, 250, 260, 255, 270, 290, 310, 305, 320, 340, 330, 350]

data = pd.Series(sales, index=dates)
print("Historisk data:")
print(data.tail())

# Dela upp i träning och test
train = data[:-3]  # Allt utom sista 3 månaderna
test = data[-3:]   # Sista 3 månaderna för validering

# Skapa och träna modell (Exponential Smoothing)
model = ExponentialSmoothing(
    train,
    seasonal_periods=12,  # Årlig säsong
    trend="add",
    seasonal="add"
).fit()

# Gör prognoser
forecast = model.forecast(6)  # 6 månader framåt
print(f"\nPrognos för kommande 6 månader:")
print(forecast.round(0))

# Utvärdera på testdata
test_forecast = model.forecast(3)
mae = np.mean(np.abs(test - test_forecast))
print(f"\nMean Absolute Error (testdata): {mae:.1f}")

# Visa jämförelse
print(f"\nJämförelse (test vs prognos):")
comparison = pd.DataFrame({
    "Faktisk": test,
    "Prognos": test_forecast.round(0)
})
print(comparison)
