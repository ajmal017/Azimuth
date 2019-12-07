import pandas
import os

path = os.path.dirname(os.path.realpath('__file__'))

path = os.getcwd()

print(path)

ohlc = pandas.read_csv("ohlcv_5years.csv")

print(ohlc)

ohlc.columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']

ohlc = ohlc[ohlc["date"] != "Date"]

ohlc = ohlc[ohlc['volume'] != '0']

print(ohlc)

ohlc = ohlc.drop(columns=["symbol"])

ohlc.to_csv(path + "/ohlcv_5yrs_cleaned.csv", index=False)

print(ohlc)
