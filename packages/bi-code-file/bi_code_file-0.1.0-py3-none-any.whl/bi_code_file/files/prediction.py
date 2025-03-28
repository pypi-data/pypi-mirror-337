from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import pandas as pd

series = read_csv('./dataset/Daily_minimum_temps.csv', header=0, index_col=0)

series = series.apply(pd.to_numeric, errors='coerce')

series.dropna(inplace=True)

series = series.iloc[:100]
X = series.values.flatten().astype(float)  # Ensure it's numeric

train, test = X[:-7], X[-7:]

model = AutoReg(train, lags=7)
model_fit = model.fit()

print(f'Lag: {model_fit.ar_lags}')
print(f'Coefficients: {model_fit.params}')

predictions = model_fit.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)

for i in range(len(predictions)):
    print(f'predicted={predictions[i]:.3f}, expected={float(test[i]):.3f}')  # Convert test[i] to float

rmse = sqrt(mean_squared_error(test, predictions))
print(f'Test RMSE: {rmse:.3f}')

pyplot.plot(range(len(test)), test, label='Actual')
pyplot.plot(range(len(test)), predictions, color='red', linestyle='dashed', label='Predictions')
pyplot.legend()
pyplot.show()
