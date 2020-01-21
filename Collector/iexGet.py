import datetime
import pandas
import urllib
import json
import time
import sys
import datetime
import time
import requests
from yahoo_earnings_calendar import YahooEarningsCalendar
import numpy as np

import os
today = datetime.date.today()

print(today)

path = os.getcwd()

today = datetime.date.today()

path = os.getcwd()

#get data from bloomberg
def get_data(url):
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	file = response.read()
	result = json.loads(file)
	result = pandas.DataFrame([result])
	return result

sandbox = "https://sandbox.iexapis.com"

sb_api_key = "Tpk_db75edaa9a9b4b2891dff83893eff6d6"

production = "https://cloud.iexapis.com/"

prod_api_key = "pk_1de77928d18b46e1b733bfa018321964"


base = datetime.datetime.today()

date_calendar = [base + datetime.timedelta(days=x) for x in range(7)]

date_from = date_calendar[0].date()

date_to = date_calendar[-1].date()

yec = YahooEarningsCalendar()

earnings = yec.earnings_between(date_from, date_to)

earnings = json.dumps(earnings)

earnings = json.loads(earnings)

eps_df = pandas.DataFrame.from_records(earnings)

ticker_ary = []
epsEstimate = []
marketCap = []
peRatio = []
price = []
debt = []
priceToSales = []
priceToBook = []
sharesOutstanding = []
day5ChangePercent = []

for i in range(len(eps_df)):


	ticker = eps_df['ticker'].loc[i]
	price_url = "https://sandbox.iexapis.com/v1/stock/{}/quote/?token=Tpk_db75edaa9a9b4b2891dff83893eff6d6".format(str(eps_df['ticker'].loc[i]).lower())
	price_result = get_data(price_url)
	stats_url = "https://sandbox.iexapis.com/v1/stock/{}/advanced-stats/?token=Tpk_db75edaa9a9b4b2891dff83893eff6d6".format(str(eps_df['ticker'].loc[i]).lower())
	stats_result = get_data(stats_url)

	try:
		priceToSales.append(stats_result["priceToSales"].values[0])
		priceToBook.append(stats_result["priceToBook"].values[0])
		sharesOutstanding.append(stats_result["sharesOutstanding"].values[0])
		day5ChangePercent.append(stats_result["day5ChangePercent"].values[0])
		debt.append(stats_result["currentDebt"].values[0])
		epsEstimate.append(eps_df['epsestimate'].loc[i])
		marketCap.append(price_result["marketCap"].values[0])
		peRatio.append(price_result["peRatio"].values[0])
		price.append(price_result["latestPrice"].values[0])
		ticker_ary.append(ticker)
		print(i)
	except Exception as e:
		print(e)
		pass



print(len(ticker_ary), len(marketCap), len(peRatio), len(price), len(debt), len(priceToSales), len(priceToBook), len(sharesOutstanding), len(day5ChangePercent))

fin_analysis = pandas.DataFrame({"ticker": ticker_ary, "epsEstimate": epsEstimate, "marketCap": marketCap, "peRatio": peRatio, "price": price, "debt": debt, "priceToSales": priceToSales , "priceToBook" : priceToBook, "sharesOutstanding" : sharesOutstanding, "day5ChangePercent" : day5ChangePercent})

fin_analysis["epsEstimate"] = fin_analysis["epsEstimate"].fillna(value = -1)
fin_analysis["price"] = fin_analysis["price"].fillna(value = -1)
fin_analysis["peRatio"] = fin_analysis["peRatio"].fillna(value = -1)
fin_analysis["priceToBook"] = fin_analysis["priceToBook"].fillna(value = -1)
fin_analysis["priceToSales"] = fin_analysis["priceToSales"].fillna(value = -1)
fin_analysis["debt"] = fin_analysis["debt"].fillna(value = -1)
fin_analysis["day5ChangePercent"] = fin_analysis["day5ChangePercent"].fillna(value = -1)



fin_analysis.to_csv(path + "/Collector/Raw/iex_raw_metrics-.csv")
