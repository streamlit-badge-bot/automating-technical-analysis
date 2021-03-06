from _plotly_future_ import v4_subplots
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime as dt
import pandas as pd

def prediction_graph(Stock, ticker, data, action_model_prediction, price_model_prediction, indication, start_date, interval):

    indicators = {'General Analysis':'General_Action', 
                    'Distinct Analysis':'Distinct_Action', 
                    'Model Prediction':'Model_Predictions'}

    prediction_length = action_model_prediction.shape[0]
    df = data.iloc[-prediction_length:]
    df['Model_Predictions'] = action_model_prediction
    df = df[['Adj Close', 'Volume', 'General_Action', 'Distinct_Action', 'Model_Predictions', 'Future_Adj_Close']]
    df = df.iloc[-366:]

    interval_value = int(interval.split()[0])
    interval_time = str(interval.split()[1]).lower()

    future_date = []
    for value in range(1, 34):
        if interval_time == 'minute':
            future_date.append(start_date + dt.timedelta(minutes = value * interval_value))
        elif interval_time == 'hour':
            future_date.append(start_date + dt.timedelta(hours = value * interval_value))
        elif interval_time == 'day':
            future_date.append(start_date + dt.timedelta(days = value * interval_value))
        elif interval_time == 'week':
            future_date.append(start_date + dt.timedelta(weeks = value * interval_value))

    df_future_price = pd.DataFrame(future_date, columns = ['Date'])
    df_future_price['Future Price'] = price_model_prediction[-33:].reshape(-1)
    df_future_price.set_index('Date', inplace = True)  

    for indicator, column_name in indicators.items():
         if indication == indicator:
            column = column_name

    df['Price_Buy'] = df[df[column] == 'Buy']['Adj Close']
    df['Price_Sell'] = df[df[column] == 'Sell']['Adj Close']

    fig = make_subplots(specs = [[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(x = df.index, y = df['Adj Close'], name = "Close Price", connectgaps = False,  marker = dict(color = '#000000')), 
    secondary_y = False)
    fig.add_trace(go.Scatter(x = df_future_price.index, y = df_future_price['Future Price'], name = "Furture Price", connectgaps = False,
    marker = dict(color = '#A9A9A9', size = 6)), secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, y = df['Price_Buy'], mode = 'markers', name = "Buy",  marker = dict(color = '#32AB60', opacity = 0.8, size = 7.5)), 
    secondary_y = False)
    fig.add_trace(go.Scatter(x = df.index, y = df['Price_Sell'], mode = 'markers', name = "Sell", marker = dict(color = '#DB4052', opacity = 0.8, size = 7.5)), 
    secondary_y = False)
    fig.add_trace(go.Bar(x = df.index, y = df['Volume'], name = "Volume", marker = dict(color = '#5DADE2', opacity = 0.45)), secondary_y = True)
    
    fig.update_layout(autosize = False, height = 750, dragmode = False, hovermode = 'x', plot_bgcolor = '#ECF0F1',
    title = dict(text = f"{Stock} to {ticker}.", y = 0.95, x = 0.5, xanchor =  'center', yanchor = 'top', font = dict(size = 20)))

    fig.update_xaxes(title_text = "Date", showline = True, linewidth = 2, linecolor = '#000000', rangeslider_visible = True, range = [df.index.min(), df_future_price.index.max()])
    fig.update_yaxes(title_text = "Close Price & Action", secondary_y = False, showline = True, linewidth = 2, linecolor = '#000000')
    fig.update_yaxes(title_text = "Volume", secondary_y = True, showline = True, linewidth = 2, linecolor = '#000000')

    return fig

def technical_analysis_graph(df):

    df = df.iloc[-366:]

    fig = make_subplots(rows = 3, cols = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['MACD'], name = "MACD", marker = dict(color = '#2ECC71')), row = 1, col = 1)
    fig.append_trace(go.Scatter(x = df.index, y = df['MACDS'], name = "MACDS", marker = dict(color = '#E74C3C')), row = 1, col = 1)
    fig.append_trace(go.Bar(x = df.index, y = df['MACDH'], name = "MACDH", marker = dict(color = '#000000')), row = 1, col = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['RSI'], name = "RSI", marker = dict(color = '#A569BD')), row = 2, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 30, y1 = 30, line = dict(color = '#008000', width = 1), row = 2, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 70, y1 = 70, line = dict(color = '#FF0000', width = 1), row = 2, col = 1)

    fig.append_trace(go.Scatter(x = df.index, y = df['SR_K'], name = "Stochastic K", marker = dict(color = '#F39C12')), row = 3, col = 1)
    fig.append_trace(go.Scatter(x = df.index, y = df['SR_D'], name = "Stochastic D", marker = dict(color = '#3780BF')), row = 3, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 20, y1 = 20, line = dict(color = '#008000', width = 1), row = 3, col = 1)
    fig.add_shape(type = 'line', x0 = df.index.min(), x1 = df.index.max(), y0 = 80, y1 = 80, line = dict(color = '#FF0000', width = 1), row = 3, col = 1)

    fig.update_layout(autosize = False, height = 750, dragmode = False, hovermode = 'x', plot_bgcolor = '#ECF0F1', 
    title = dict(text = "Technical Analysis.", y = 0.95, x = 0.5, xanchor = 'center', yanchor = 'top', font = dict(size = 20)))

    fig.update_shapes(dict(opacity = 0.7))
    fig.update_xaxes(showgrid = True, zeroline = True, showline = True, linewidth = 2, linecolor = '#000000')
    fig.update_xaxes(title_text = "Date", row = 3, col = 1)
    fig.update_yaxes(zeroline = True, showline = True, linewidth = 2, linecolor = '#000000')
    fig.update_yaxes(title_text = "MACD", row = 1, col = 1)
    fig.update_yaxes(title_text = "RSI", range = [0, 100], tickvals = [0, 30, 70, 100], row = 2, col = 1)
    fig.update_yaxes(title_text = "%K & %D", range = [-1, 101], tickvals = [0, 20, 80, 100], row = 3, col = 1)

    return fig