import requests
import json
import pandas as pd
import datetime as dt
import yfinance as yf
import time

def date_utc(date_):

    date_ = pd.to_datetime(date_, utc = True)
    date_ = date_.dt.tz_localize(None)
    return date_

def binance_market_data(ticker, market, interval):

    try:
        url = f"https://api.binance.com/api/v1/klines?symbol={ticker}{market}&interval={interval}"
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = ['open_time', 'Open', 'High', 'Low', 'Adj Close', 'Volume', 'close_time', 
                        'quoted average volume', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']
        df['Date'] = [dt.datetime.fromtimestamp(x/1000.0).replace(microsecond = 0) for x in df.close_time]
        df['Date'] = date_utc(df['Date'])
        df.drop(['open_time', 'close_time', 'quoted average volume', 'taker_base_vol', 
                'ignore', 'num_trades', 'taker_quote_vol'], axis = 1, inplace = True)
        df.set_index('Date', inplace = True)
        df = df[['High', 'Low', 'Open', 'Volume', 'Adj Close']].apply(pd.to_numeric)

        return df

    except (ValueError, KeyError, ConnectionError, AttributeError) as e:
            print ("Whoops!! Something seems to have gone wrong. Please try again..")
            pass

def bitfinex_market_data(ticker, market, interval):

    try:
        url = f"https://api-pub.bitfinex.com/v2/candles/trade:{interval}:t{ticker}{market}/hist"
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = ['MTS', 'Open', 'Adj Close', 'High', 'Low', 'Volume']
        df['Date'] = [dt.datetime.fromtimestamp(x/1000.0) for x in df.MTS]
        df['Date'] = date_utc(df['Date'])
        df.set_index('Date', inplace = True)
        df = df[['High', 'Low', 'Open', 'Volume', 'Adj Close']]

        return df
        
    except (ValueError, KeyError, ConnectionError, AttributeError) as e:
            print ("Whoops!! Something seems to have gone wrong. Please try again..")
            pass

def bittrex_market_data(ticker, market, interval):
    
    try:
        url = f"https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={market}-{ticker}&tickInterval={interval}"
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data['result'])
        df.rename(columns = {'O':'Open', 'H':'High', 'L':'Low', 'C':'Adj Close', 'V':'Volume', 
                             'BV':'Base Volume', 'T':'Date'}, inplace = True)
        df['Date'] = df['Date'].apply(lambda x: x.replace('T', ' '))
        df['Date'] = date_utc(df['Date'])
        df.set_index('Date', inplace = True)
        df = df[['High', 'Low', 'Open', 'Volume', 'Adj Close']]
        
        return df
    
    except (ValueError, KeyError, ConnectionError, AttributeError) as e:
            print ("Whoops!! Something seems to have gone wrong. Please try again..")
            pass

def yahoo_market_data(ticker, period, interval):

    try:
        df = yf.download(tickers = ticker, period = period, interval = interval, auto_adjust = True,
                prepost = True, threads = True, proxy = None)
        df = df.reset_index()
        df.rename(columns = {'Datetime':'Date', 'Close': 'Adj Close'}, inplace = True)
        df['Date'] = date_utc(df['Date'])
        df.set_index('Date', inplace = True)
        df = df[['High', 'Low', 'Open', 'Volume', 'Adj Close']]

        return df

    except (ValueError, KeyError, ConnectionError, AttributeError) as e:
            print ("Whoops!! Something seems to have gone wrong. Please try again..")
            pass