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
import requests as r 

def get_income_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/financials/income-statement/" + t + "?period=quarter")
    return json.loads(req.text)
    

def get_balancesheets_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + t + "?period=quarter")
    return json.loads(req.text)


def get_cashflow_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/" + t + "?period=quarter")
    return json.loads(req.text)


def get_ev_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/enterprise-value/" + t + "?period=quarter")
    return json.loads(req.text)


def get_metrics_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/company-key-metrics/" + t + "?period=quarter")
    return json.loads(req.text)

def get_comp_profile(t):
    req = r.get("https://financialmodelingprep.com/api/v3/company/profile/" + t)
    return json.loads(req.text)


def get_valuation(t):
    metric_data_q = get_metrics_q(t)['metrics'][0]
    income_data_q = get_income_q(t)['financials'][0]
    profile_data_q = get_comp_profile(t)['profile']
    balance_data_q = get_balancesheets_q(t)['financials'][0]
    value_metrics =  {
                "ticker": t,
                "price": profile_data_q['price'],
                "p_e": metric_data_q["PE ratio"],
                "p_b": metric_data_q["PB ratio"],
                "p_s": metric_data_q["Price to Sales Ratio"],
                "sharesoutsanding": income_data_q['Weighted Average Shs Out'],
                "eps": income_data_q["EPS"], 
                "net_debt": balance_data_q['Net Debt'],
                "ncavps": (balance_data_q['Total current assets'] - balance_data_q['Total current liabialities']) / float(income_data_q['Weighted Average Shs Out']),
                "debt_to_asset": metric_data_q['Debt to Assets'],
                "p_eps":profile_data_q['price'] /  income_data_q["EPS"],
                "gross_profit": income_data_q["Gross Margin"],
                "revenue_earnings": income_data_q['Net Income'] / balance_data_q["Total shareholders equity"]
                
            }
    
    value_metrics = pandas.io.json.json_normalize(value_metrics)

    return value_metrics


#get data from bloomberg
def get_data(url):
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	file = response.read()
	result = json.loads(file)
	result = pandas.DataFrame([result])
	return result


today = datetime.date.today()


path = os.getcwd()

today = datetime.date.today()

path = os.getcwd()

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

# fin_analysis["epsEstimate"] = fin_analysis["epsEstimate"].fillna(value = -1)
# fin_analysis["price"] = fin_analysis["price"].fillna(value = -1)
# fin_analysis["peRatio"] = fin_analysis["peRatio"].fillna(value = -1)
# fin_analysis["priceToBook"] = fin_analysis["priceToBook"].fillna(value = -1)
# fin_analysis["priceToSales"] = fin_analysis["priceToSales"].fillna(value = -1)
# fin_analysis["debt"] = fin_analysis["debt"].fillna(value = -1)
# fin_analysis["day5ChangePercent"] = fin_analysis["day5ChangePercent"].fillna(value = -1)


fin = fin_analysis[fin_analysis["epsEstimate"] > 0 ]
fin = fin_analysis[(fin_analysis["price"] < 50) & (fin_analysis["price"] > 0)]
fin = fin_analysis[(fin_analysis["peRatio"] < 11) & (fin_analysis["peRatio"] != -1)]
fin = fin_analysis[fin_analysis["priceToBook"] < 10]
fin = fin_analysis[fin_analysis["priceToSales"] < 10 & (fin_analysis["priceToSales"] > 0)]
fin = fin_analysis[fin_analysis["debt"] > 0]
fin = fin_analysis[fin_analysis["day5ChangePercent"] > 0]



fin_analysis.to_csv(path + "/Collector/Raw/iex_raw_metrics-.csv")
