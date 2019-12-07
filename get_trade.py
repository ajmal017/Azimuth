import pandas
import urllib2
import json
import datetime
import pandas
import urllib2
import json
import pymongo
import time
import sys
import datetime
from datetime import date, timedelta
import pymongo
import collections
from bson.json_util import loads
import pandas as pd
import math as m
import numpy as np
import talib
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)




def get_data(url):
	req = urllib.request.Request(url)
	response = urllib.request.urlopen(req)
	file = response.read()
	result = json.loads(file)
	result = pandas.DataFrame.from_records(result)
	return result


def get_tickers(date):
	#query the mongodb database by a timestamp

	df = db.fin_analysis.find({"_id" : date})
	document = None


	#sort through mongodb pre_market_eps database for stock tickers
	for i in df:
		print(i.keys())
		ticker = i['ticker'][0]

		return ticker



client = pymongo.MongoClient('localhost', 27017)

db = client.fin

datelist = pandas.bdate_range(pandas.datetime.today(), periods=5, freq='B').tolist()

datelist = [str(id) for id in db.fin_analysis.find().distinct('_id')]

date = []

for i in range(0, len(datelist)):
	date.append(str(datelist[i]).split(" ", 1)[0])

before_date = []
after_date = []
after_signal_con = []
MOM_signal_con = []
ROC_signal_con = []
MACD_signal_con = []
ADX_signal_con = []
RSI_signal_con = []
MACD_1 = []
MACD_2 = []
MACD_3 = []
ADX_1 = []
ADX_2 = []
ADX_3 = []
ADX_4 = []
ADX_5 = []
RSI_1 = []
RSI_2 = []
RSI_3 = []
RSI_4 = []
RSI_5 = []
ROC_1 = []
ROC_2 = []
ROC_3 = []
ROC_4 = []
ROC_5 = []
MOM_1 = []
MOM_2 = []
MOM_3 = []
MOM_4 = []
MOM_5  = []
ticker = []


for tick in range(len(date)):
	tickers = get_tickers(date[tick])
	print(len(tickers))


	for i_tickers in range(len(tickers)):
		filing_date = datetime.datetime.strptime(date[tick], "%Y-%m-%d")
		days_before = (filing_date - timedelta(days=36)).isoformat()
		dates_before = pandas.bdate_range(days_before, periods=26, freq='B').format()




		# print(dates_after)

		dates_before_period_end = dates_before[-1]
		dates_before_period_start = dates_before[0]


		open_prices_before = "https://api.intrinio.com/historical_data?identifier={}&item=open_price&start_date={}&end_date={}&api_key=OjYyYjg0OGZjYzliYjdiMGNkZjQ5YjE0MmIzNDdlMmZl".format(tickers[i_tickers], dates_before_period_start, dates_before_period_end)
		close_prices_before = "https://api.intrinio.com/historical_data?identifier={}&item=close_price&start_date={}&end_date={}&api_key=OjYyYjg0OGZjYzliYjdiMGNkZjQ5YjE0MmIzNDdlMmZl".format(tickers[i_tickers], dates_before_period_start, dates_before_period_end)

		high_prices  = "https://api.intrinio.com/historical_data?identifier={}&item=high_price&start_date={}&end_date={}&api_key=OjYyYjg0OGZjYzliYjdiMGNkZjQ5YjE0MmIzNDdlMmZl".format(tickers[i_tickers], dates_before_period_start, dates_before_period_end)
		low_prices  = "https://api.intrinio.com/historical_data?identifier={}&item=low_price&start_date={}&end_date={}&api_key=OjYyYjg0OGZjYzliYjdiMGNkZjQ5YjE0MmIzNDdlMmZl".format(tickers[i_tickers], dates_before_period_start, dates_before_period_end)



		ticker.append(tickers[i_tickers])



		# open_prices_before = get_data(open_prices_before)
		# open_prices_after = get_data(open_prices_after)

		close_prices_before = get_data(close_prices_before)
		# close_prices_after = get_data(close_prices_after)

		# volume_before = get_data(volume_before)
		# volume_after = get_data(volume_after)

		high_before = get_data(high_prices)
		low_before = get_data(low_prices)

		# close_dataframe = pandas.DataFrame({})

		data = {}
		after_close = []
		before_close = []
		high = []
		low = []
		for k in range(len(close_prices_before["data"][:])):

			before_close.append(close_prices_before["data"][:][k].values()[1])

			# print(before_close)

			# before_date.append(close_prices_before["data"][:][k].values()[0])

			high.append(high_before["data"][:][k].values()[1])

			low.append(low_before["data"][:][k].values()[1])

			if (len(high) == len(close_prices_before["data"][:])):
				try:
					# close_dataframe = pandas.DataFrame({})
					high = list(reversed(high))

					low = list(reversed(low))


					print("Before")
					before_close = list(reversed(before_close))

					# print(before_date)

					data = {"Close": before_close, "High" : high, "Low" : low}

					df = pandas.DataFrame(data)

					# print(df)
					# print(close_dataframe)

					# MACD = MACD(close_dataframe, 13, 26)


					n_fast = 13
					n_slow = 26



					EMAfast = pd.Series(pd.ewma(df['Close'], span = n_fast))
					EMAslow = pd.Series(pd.ewma(df['Close'], span = n_slow))
					MACD = pd.Series(EMAfast - EMAslow, name = 'MACD_' + str(n_fast) + '_' + str(n_slow))
					MACDsign = pd.Series(pd.ewma(MACD, span = 9, min_periods = 8), name = 'MACDsign_' + str(n_fast) + '_' + str(n_slow))
					MACDdiff = pd.Series(MACD - MACDsign, name = 'MACDdiff_' + str(n_fast) + '_' + str(n_slow))
					df = df.join(MACD)
					df = df.join(MACDsign)
					df = df.join(MACDdiff)

					print(df["MACDdiff_13_26"])


					MACD_signal = df["MACDdiff_13_26"].dropna().tolist()[-1] > 0

					MACD_1.append(df["MACDdiff_13_26"].dropna().tolist()[-1])
					MACD_2.append( df["MACDdiff_13_26"].dropna().tolist()[-2])
					MACD_3.append(df["MACDdiff_13_26"].dropna().tolist()[-3])

					# print(MACD_signal)

					MACD_signal_con.append(MACD_signal)


					# print(df)

					n = 7

					n_ADX = 1

					i = 0
					UpI = []
					DoI = []
					while i + 1 <= df.index[-1]:
					    UpMove = df.get_value(i + 1, 'High') - df.get_value(i, 'High')
					    DoMove = df.get_value(i, 'Low') - df.get_value(i + 1, 'Low')
					    if UpMove > DoMove and UpMove > 0:
					        UpD = UpMove
					    else: UpD = 0
					    UpI.append(UpD)
					    if DoMove > UpMove and DoMove > 0:
					        DoD = DoMove
					    else: DoD = 0
					    DoI.append(DoD)
					    i = i + 1
					i = 0
					TR_l = [0]
					while i < df.index[-1]:
					    TR = max(df.get_value(i + 1, 'High'), df.get_value(i, 'Close')) - min(df.get_value(i + 1, 'Low'), df.get_value(i, 'Close'))
					    TR_l.append(TR)
					    i = i + 1
					TR_s = pd.Series(TR_l)
					ATR = pd.Series(pd.ewma(TR_s, span = n, min_periods = n))
					UpI = pd.Series(UpI)
					DoI = pd.Series(DoI)
					PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1) / ATR)
					NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1) / ATR)
					ADX = pd.Series(pd.ewma(abs(PosDI - NegDI) / (PosDI + NegDI), span = n_ADX, min_periods = n_ADX - 1), name = 'ADX_' + str(n) + '_' + str(n_ADX))
					df = df.join(ADX)

					# print(df["ADX_7_1"])

					ADX_signal = df["ADX_7_1"].dropna().tolist()[-1] > .50
					#and df["ADX_7_1"].dropna().tolist()[-1] > .65

					ADX_signal_con.append(ADX_signal)


					ADX_1.append(df["ADX_7_1"].dropna().tolist()[-1])
					ADX_2.append( df["ADX_7_1"].dropna().tolist()[-2])
					ADX_3.append(df["ADX_7_1"].dropna().tolist()[-3])
					ADX_4.append( df["ADX_7_1"].dropna().tolist()[-4])
					ADX_5.append(df["ADX_7_1"].dropna().tolist()[-5])



					n = 7

					i = 0
					UpI = [0]
					DoI = [0]
					while i + 1 <= df.index[-1]:
					    UpMove = df.get_value(i + 1, 'High') - df.get_value(i, 'High')
					    DoMove = df.get_value(i, 'Low') - df.get_value(i + 1, 'Low')
					    if UpMove > DoMove and UpMove > 0:
					        UpD = UpMove
					    else: UpD = 0
					    UpI.append(UpD)
					    if DoMove > UpMove and DoMove > 0:
					        DoD = DoMove
					    else: DoD = 0
					    DoI.append(DoD)
					    i = i + 1
					UpI = pd.Series(UpI)
					DoI = pd.Series(DoI)
					PosDI = pd.Series(pd.ewma(UpI, span = n, min_periods = n - 1))
					NegDI = pd.Series(pd.ewma(DoI, span = n, min_periods = n - 1))
					RSI = pd.Series(PosDI / (PosDI + NegDI), name = 'RSI_' + str(n))
					df = df.join(RSI)


					RSI_signal = df["RSI_7"].dropna().tolist()[-1]  > .50 and df["RSI_7"].dropna().tolist()[-1] < .80



					RSI_signal_con.append(RSI_signal)

					RSI_1.append(df["RSI_7"].dropna().tolist()[-1])
					RSI_2.append( df["RSI_7"].dropna().tolist()[-2])
					RSI_3.append(df["RSI_7"].dropna().tolist()[-3])
					RSI_4.append( df["RSI_7"].dropna().tolist()[-4])
					RSI_5.append(df["RSI_7"].dropna().tolist()[-5])



					n = 5

					M = df['Close'].diff(n - 1)
					N = df['Close'].shift(n - 1)
					ROC = pd.Series(M / N, name = 'ROC_' + str(n))
					df = df.join(ROC)




					ROC = df["ROC_5"].dropna().tolist()[-5:]



					y = np.array([1,2,3,4,5])

					ROC = np.array(ROC)
					coeffs = np.polyfit(ROC, y, 1)
					ROC_slope = coeffs[-2]
					ROC_signal = ROC_slope > 0

					ROC_signal_con.append(ROC_signal)

					ROC_1.append(df["ROC_5"].dropna().tolist()[-1])
					ROC_2.append( df["ROC_5"].dropna().tolist()[-2])
					ROC_3.append(df["ROC_5"].dropna().tolist()[-3])
					ROC_4.append( df["ROC_5"].dropna().tolist()[-4])
					ROC_5.append(df["ROC_5"].dropna().tolist()[-5])

					n = 14


					M = pd.Series(df['Close'].diff(n), name = 'Momentum_' + str(n))
					df = df.join(M)


					MOM = df["Momentum_14"].dropna().tolist()[-5:]
					MOM = np.array(MOM)
					coeffs = np.polyfit(MOM, y, 1)
					MOM_slope = coeffs[-2]
					MOM_signal = MOM_slope > 0

					MOM_signal_con.append(MOM_signal)

					MOM_1.append(df["Momentum_14"].dropna().tolist()[-1])
					MOM_2.append( df["Momentum_14"].dropna().tolist()[-2])
					MOM_3.append(df["Momentum_14"].dropna().tolist()[-3])
					MOM_4.append( df["Momentum_14"].dropna().tolist()[-4])
					MOM_5.append(df["Momentum_14"].dropna().tolist()[-5])
				except:
					pass



			else:
				pass

		# for k in range(len(close_prices_after["data"][:])):
		# 	y = np.array([1,2,3,4,5,6,7])
		# 	after_close.append(close_prices_after["data"][:][k].values()[1])

		# 	if(len(close_prices_after["data"][:]) == len(after_close)):

		# 		after_close = list(reversed(after_close))
		# 		after_trend = np.array(after_close[-7:])
		# 		print(len(after_trend))

		# 		try:
		# 			coeffs = np.polyfit(after_trend, y, 1)
		# 			after_trend = coeffs[-2]
		# 			after_signal = after_trend > 0
		# 			after_signal_con.append(after_signal)
		# 		except:
		# 			after_signal_con.append("Check")


print(len(after_signal_con))
print(len(MOM_signal_con))
print(len(ROC_signal_con))
print(len(MACD_signal_con))
print(len(ADX_signal_con))
print(len(RSI_signal_con))
print(len(MACD_1))
print(len(MACD_2))
print(len(MACD_3))
print(len(ADX_1))
print(len(ADX_2))
print(len(ADX_3))
print(len(ADX_4))
print(len(ADX_5))
print(len(RSI_1))
print(len(RSI_2))
print(len(RSI_3))
print(len(RSI_4))
print(len(RSI_5))
print(len(ROC_1))
print(len(ROC_2))
print(len(ROC_3))
print(len(ROC_4))
print(len(ROC_5))
print(len(MOM_1))
print(len(MOM_2))
print(len(MOM_3))
print(len(MOM_4))
print(len(MOM_5))


final_features = pandas.DataFrame({"ROC_1" : ROC_1,  "ROC_2" : ROC_2, "ROC_3" : ROC_3,  "ROC_4" : ROC_4, "ROC_5" : ROC_5, "RSI" : RSI_signal_con,  "RSI_1" : RSI_1,  "RSI_2" : RSI_2, "RSI_3" : RSI_3,  "RSI_4" : RSI_4, "RSI_5" : RSI_5, "MOM" : MOM_signal_con, "MOM_1" : MOM_1,  "MOM_2" : MOM_2, "MOM_3" : MOM_3,  "MOM_4" : MOM_4, "MOM_5" : MOM_5, "ADX" : ADX_signal_con, "ADX_1" : ADX_1,  "ADX_2" : ADX_2, "ADX_3" : ADX_3,  "ADX_4" : ADX_4, "ADX_5" : ADX_5, "MACD" : MACD_signal_con, "MACD_1" : MACD_1,  "MACD_2" : MACD_2, "MACD_3" : MACD_3})

final_features.to_csv("targets.csv")


# # print(talib.ADX(close_dataframe["Close"].values, close_dataframe["High"].values, close_dataframe["Low"].values, 10))




		# print(get_data(prices_after))


		# print(dates_before)






# for i in x
# "https://stockrow.com/api/companies/HOME/financials_overview.json?ticker={}".format(ticker)
