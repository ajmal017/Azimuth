import pandas
import json
import urllib
import requests as r 

def get_income_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/financials/income-statement/" + t + "?period=quarter")
    return json.loads(req.text)
    

def get_bs_q(t):
    req = r.get("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + t + "?period=quarter")
    return json.loads(req.text)


def get_cf_q(t):
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
    cashflow_data_q = get_cf_q(t)['financials'][0]
    balance_data_q = get_bs_q(t)['financials'][0]
    value_metrics =  {
                "ticker": t,
                "price": profile_data_q['price'],
                "p_e": metric_data_q["PE ratio"],
                "p_b": metric_data_q["PB ratio"],
                "p_s": metric_data_q["Price to Sales Ratio"],
                "ebita_ev": metric_data_q["Enterprise Value over EBITDA"],
                "sharesoutsanding": income_data_q['Weighted Average Shs Out'],
                "eps": income_data_q["EPS"],
                "P/cashflow": profile_data_q["price"] / (float(cashflow_data_q["Free Cash Flow"])/ 4.53e9),
                "net_debt": balance_data_q['Net Devt']
            }

    return value_metrics






