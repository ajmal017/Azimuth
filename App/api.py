from lxml import html
import requests
import ast
import json
import matplotlib.pyplot as plt
import urllib.request
import re
from datetime import datetime, timedelta
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
import pandas
import ast


def nasdaq_parse():

    base = datetime.datetime.today()

    date_calendar = [base + timedelta(days=x) for x in range(7)]

    date_from = date_calendar[0].date()

    date_to = date_calendar[-1].date()

    yec = YahooEarningsCalendar()

    earnings = yec.earnings_between(date_from, date_to)

    earnings = json.dumps(earnings)

    earnings = json.loads(earnings)

    eps_df = pandas.DataFrame.from_records(earnings)

    eps_df = eps_df[['companyshortname', 'ticker']]

    eps_dict = eps_df.to_dict('records')

    # eps_df = eps_df.to_dict('records')

    """
    Get a list of the top 100 companies listed on NASDAQ
    """
    companies_list = [{'label': i['companyshortname'], 'value': i['ticker']} for i in eps_dict]

    return companies_list


def format_nasdaq(companies):
    """
    Convert the parsed companies list to format that is interpretable by dash_core_components.dropdown
    """
    companies_list = ast.literal_eval(companies)
    options=[]
    # Get the company name and symbol.
    for i in range(len(companies_list)):
        new_company = {'label': companies_list[i][1], 'value': companies_list[i][0]}
        options.append(new_company)

    return options


def get_stocks_daily(company_symbols):
    """
    Make API call to get the stock variations of the selected companies
    """
    # Get the api key
    # api_key = get_api_key("alphavantage")
    # Make the request
    contents = urllib.request.urlopen("https://www.alphavantage.co/query?function="
    + "TIME_SERIES_DAILY&symbol=" + company_symbols + "&apikey=" + "VMK9SEQ8ZJH3PZU5").read()
    # Parse it
    json_res = json.loads(contents)
    series = json_res["Time Series (Daily)"]
    days = [day for day in series]
    closing = [series[day]["4. close"] for day in days]

    return days, closing


def get_hidden_stocks_daily(company_symbols):
    """
    Make API call to get the stock variations of the selected companies and returns
    it in JSON format
    """
    # Get the api key
    # api_key = get_api_key("alphavantage")
    # Make the request
    contents = urllib.request.urlopen("https://www.alphavantage.co/query?function="
    + "TIME_SERIES_DAILY&symbol=" + company_symbols + "&apikey=" + "VMK9SEQ8ZJH3PZU5").read()
    return contents


def get_stocks_intraday(company_symbols):
    """
    Make API call to get the stock variations of the selected companies
    """
    # Get the api key
    # api_key = get_api_key("alphavantage")
    # Make the request
    contents = urllib.request.urlopen("https://www.alphavantage.co/query?function="
    + "TIME_SERIES_INTRADAY&symbol=" + company_symbols + "&interval=5min&apikey="
    + "VMK9SEQ8ZJH3PZU5").read()
    # Parse it
    json_res = json.loads(contents)
    series = json_res["Time Series (5min)"]
    days = [day for day in series]
    closing = [series[day]["4. close"] for day in days]

    return days, closing


def get_news_sources():
    """
    Function to get all the support News Sources in English.
    """
    # Get the api key
    # api_key = get_api_key("newsapi")

    # Make the API call
    response = requests.get('https://newsapi.org/v2/sources?language=en&apiKey=' + "13e31613acb54afc88ea8e54f1832d9a")
    json_res = response.json()["sources"]
    sources = [[source["name"]] for source in json_res]
    ids = [source["id"] for source in json_res]

    options=[]
    # Get the company name and symbol
    for i in range(len(sources)):
        new_source = {'label': sources[i][0], 'value': ids[i]}
        options.append(new_source)

    return options


def format_companies(company):
    """
    Format the selected company so that the API can find relevant articles.
    """
    # Get the company names and symbols
    nasdaq = nasdaq_parse()
    # Find the right company name given the symbol
    formatted_companies = ""
    for nasdaq_company in nasdaq:
        if(nasdaq_company['value'] == company):
            # Remove junk at the end of the names
            if(nasdaq_company['label'][-6:] == ", Inc."):
                return re.sub(r' ', "-", nasdaq_company['label'][:-6])

            if(nasdaq_company['label'][-5:] == ", Inc"):
                return re.sub(r' ', "-", nasdaq_company['label'][:-5])

            if(nasdaq_company['label'][-5:] == " Inc."):
                return re.sub(r' ', "-", nasdaq_company['label'][:-5])

            return re.sub(r' ', "-", nasdaq_company['label'])


def format_sources(sources):
    """
    Make a comma separated string of news source labels.
    """
    formatted_sources = ""
    for source in sources:
        formatted_sources += source["value"] + ','

    return formatted_sources


def get_articles(company):
    """
    Function that makes the api calls given company names.
    """
    # Get the news sources
    sources = get_news_sources()
    # Format the news sources
    formatted_sources = format_sources(sources)
    # Format the companies
    formatted_company = format_companies(company)
    # Get the api key
    # api_key = get_api_key("newsapi")
    # Create a timespan : 14 days
    end = datetime.datetime.now().strftime("%Y-%m-%d")
    start = (datetime.datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    # Get the articles
    contents = urllib.request.urlopen("http://newsapi.org/v2/everything?sources="
    + formatted_sources + "&q=" + formatted_company + "&sortBy=relevancy&from="
    + start + "&to=" + end + "&apikey=" + "13e31613acb54afc88ea8e54f1832d9a").read()

    # Parse them
    json_res = json.loads(contents)

    return json_res
