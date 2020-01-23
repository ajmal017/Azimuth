# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 12:25:30 2018

@author: Ishan Shah
"""

#Python Code
#Step 1: Import the necessary libraries.

# To get closing price data  
from pandas_datareader import data as pdr   
import fix_yahoo_finance as yf  
yf.pdr_override()   
  
# Plotting graphs  
import matplotlib.pyplot as plt  
import seaborn  
  
# Data manipulation  
import numpy as np  
import pandas as pd  

#Step 2: Define a function to calculate the strategy performance on a stock.

def strategy_performance(stock_ticker):  
    stock = pdr.get_data_yahoo(stock_ticker, start="2009-01-01", end="2017-10-01")         

    #Compute 5-days breakout and mean.

    # 5-days high  
    stock['high'] = stock.Close.shift(1).rolling(window=5).max()  
    # 5-days low  
    stock['low'] = stock.Close.shift(1).rolling(window=5).min()  
    # 5-days mean  
    stock['avg'] = stock.Close.shift(1).rolling(window=5).mean()  

    #Entry Rules
    #When the closing price of the stock is greater than the high of past 55 days 
    #then we go long on the stock and 
    #when the closing price of the stock is less than the low of past 55 days 
    #then we go short on the stock.

    stock['long_entry'] = stock.Close > stock.high         
    stock['short_entry'] = stock.Close < stock.low  


    #Exit Rules

    #We will exit the positions if the stock price crosses the mean of past 55 days.

    stock['long_exit'] = stock.Close < stock.avg  
    stock['short_exit'] = stock.Close > stock.avg  


    #Positions
    
    #We will now store the entry and exit signal in a single column. Long position is indicated by 1, short position is indicated by -1 and exit or no position is indicated by 0. We will carry forward the previous position if no position exists for a time period using the fillna method.

    stock['positions_long'] = np.nan    
    stock.loc[stock.long_entry,'positions_long']= 1    
    stock.loc[stock.long_exit,'positions_long']= 0    
    
    stock['positions_short'] = np.nan    
    stock.loc[stock.short_entry,'positions_short']= -1    
    stock.loc[stock.short_exit,'positions_short']= 0    
  
    stock['Signal'] = stock.positions_long + stock.positions_short  
  
    stock = stock.fillna(method='ffill')   


    #Strategy Returns
    
    #We have computed the log returns of the stock and multiplied with the Signal (1,-1 or 0) to get the strategy returns.

    daily_log_returns = np.log(stock.Close/stock.Close.shift(1))  
    daily_log_returns = daily_log_returns * stock.Signal.shift(1)  
  
    # Plot the distribution of 'daily_log_returns'  
    print(stock_ticker)
    daily_log_returns.hist(bins=50)  
    plt.show()  
    return daily_log_returns.cumsum() 


#Step 3: Create a portfolio of stocks and calculate the strategy performance for each stock.

portfolio = ['AAPL','KMI','F']  
cum_daily_return = pd.DataFrame()  
for stock in portfolio:   
    cum_daily_return[stock] = strategy_performance(stock)  

# Plot the cumulative daily returns  
print("Cumulative Daily Returns")
cum_daily_return.plot()  
# Show the plot  
plt.show()  
