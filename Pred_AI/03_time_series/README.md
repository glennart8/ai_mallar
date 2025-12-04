# Time Series Forecasting

Prognostisera framtida värden baserat på historisk data.

## Användning

```python
model = ExponentialSmoothing(
    data,
    seasonal_periods=12,
    trend="add",
    seasonal="add"
).fit()

forecast = model.forecast(6)  # 6 perioder framåt
```

## När använda

- Försäljningsprognoser
- Budgetplanering
- Lageroptimering
- Kapacitetsplanering
- Trafik/besökarstatistik

## Modellval

- **ExponentialSmoothing** - Bra för data med trend och säsong
- **ARIMA** - Flexibel, kräver mer tuning
- **Prophet** (Facebook) - Lättanvänd, hanterar helgdagar

## Parametrar

- `seasonal_periods` - Perioder per säsong (12 för månadsdata)
- `trend` - "add" (additiv) eller "mul" (multiplikativ)
- `seasonal` - "add" eller "mul" för säsongsvariationer

## Utvärdering

- **MAE** (Mean Absolute Error) - Genomsnittligt fel
- **MAPE** (Mean Absolute Percentage Error) - Fel i procent
- Visualisera prognos vs faktiskt utfall
