import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sp500 = yf.Ticker('SPY')

data = sp500.history(period = "max", interval="1mo") #get maximum data available for spy for 1 month intervals
data = data.reset_index()

data["Percentage Gain"] = ((data["Close"]-data["Open"])/data["Open"])*100

# data["Percentage Gain"].plot(kind="hist",bins=20)
# plt.title("Distribution of Monthly Gains")
# plt.show()

monthly_gains = data["Percentage Gain"].to_numpy()

monthly_mean = monthly_gains.mean()
monthly_std = monthly_gains.std()

upper_limit = monthly_mean + monthly_std
lower_limit = monthly_mean - monthly_std

monthly_gains_65p = []

for gain in monthly_gains: #get middle 65%
    if (gain > lower_limit and gain < upper_limit):
        monthly_gains_65p.append(float(gain))

monthly_gains_65p = np.array(monthly_gains_65p)

def get_random_values(num): #get as many random values as you need
    values = []
    for i in range(num):
        values.append(float(np.random.choice(monthly_gains_65p)))
    return values

def get_yearly_values(num):
    values = []
    for i in range(num):
        monthly_12 = get_random_values(12)
        values.append(round(float(np.sum(monthly_12)),3))
    return values

# print(get_yearly_values(10))









