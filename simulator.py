import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from datetime import datetime as dt
import yfinance as yf
import pandas_datareader.data as pdr
from sp500_values import get_yearly_values

years = 30
number_of_sim = 1000

def get_data(years):
    stock_returns = []
    for i in range(number_of_sim):
        stock_returns.append(get_yearly_values(years))
    bond_returns = float(yf.Ticker("^TNX").history(period="1d")['Close'].iloc[-1]) #current 10 year bond rate
    # yfinance fedfunds rate not working so using pd.DataReader instead
    start_date = dt(dt.now().year, 1, 1)
    end_date = dt.now()
    fedfunds_data = pdr.DataReader('DFF', 'fred', start_date, end_date)
    cash_returns = float(fedfunds_data['DFF'].iloc[-1])  # Get the most recent Federal Funds rate

    return stock_returns, bond_returns, cash_returns

stock_returns, bond_returns, cash_returns = get_data(years)
returns = [stock_returns, bond_returns, cash_returns]
# print(returns[0])
# print(get_data(10))

def calculate_stock_values(allocation, returns):
    stock_yearly_values = [allocation]
    i = 0
    for stock_return in returns:
        stock_yearly_values.append(round(stock_yearly_values[i] + stock_yearly_values[i] * (stock_return/100),2))
        i += 1
    return stock_yearly_values

def calculate_fixed_rate_values(allocation, p_return, years):
    fixed_rate_values = [allocation]
    for i in range(years):
        fixed_rate_values.append(round(fixed_rate_values[i] + fixed_rate_values[i] * (p_return/100),2))
    return fixed_rate_values

# print(calculate_fixed_rate_values(1000, 4.5, 10))


def simulate_portfolio(initial_value, allocations, returns, enable_withdrawls = False, 
                       withdrawl_rate = 0.0, enable_inflation = False, inflation_rate = 0.0):
    stock_allocation = initial_value * allocations[0]
    bond_allocation = initial_value * allocations[1]
    cash_allocation = initial_value * allocations[2]

    bond_values = calculate_fixed_rate_values(bond_allocation, returns[1], years)
    cash_values = calculate_fixed_rate_values(cash_allocation, returns[2], years)

    bond_values = np.array(bond_values)
    cash_values = np.array(cash_values)

    
    sims = []
    for i in range(number_of_sim):
        stock_values = calculate_stock_values(stock_allocation, returns[0][i])
        stock_values = np.array(stock_values)

        sims.append(np.array([stock_values, bond_values, cash_values]))

    return np.array(sims) #returns np array of (# of sims, asset classes, years)


simulations = simulate_portfolio(200000000, [.3,.6,.1], returns)

#get final values
final_values = simulations[:,:,-1]
stock_final_values = final_values[:,0]
bond_final_values = final_values[:,1]
cash_final_values = final_values[:,2]
final_portfolio_value = stock_final_values + bond_final_values + cash_final_values


plt.figure(figsize=(10,6))
plt.hist(final_portfolio_value, bins=30)
plt.show()

mean_values = np.mean(simulations, axis=0)
years_axis = np.arange(simulations.shape[2])
plt.stackplot(
    years_axis,
    mean_values[0],
    mean_values[1],
    mean_values[2],
    labels=["Stocks", "Bonds", "Cash"]
)
plt.show()

#get the median final value and all of its years
median_final_value = np.median(final_portfolio_value)
median_index = np.argmin(np.abs(final_portfolio_value - median_final_value)) 
median_sim = simulations[median_index]

plt.stackplot(
    years_axis,
    median_sim[0],
    median_sim[1],
    median_sim[2],
    labels=["Stocks", "Bonds", "Cash"]
)
plt.show()

addingVar = 123

    

        









