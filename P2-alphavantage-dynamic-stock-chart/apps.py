# -*- coding: utf-8 -*-
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import requests
import pandas as pd

# multiprocessing handel static data request
import multiprocessing
def find_stock(name):
    web.DataReader(name, 'morningstar', datetime.datetime(2015,1,1), datetime.datetime(2015,1,3))
    return

# default stock
## morningstar
defaultStock = 'GOOGL'
start = datetime.datetime(2015,1,1)
end = datetime.datetime.now()
defaultdf = web.DataReader(defaultStock, 'morningstar', start, end)
## alphavantage
alpha_API_URL = "https://www.alphavantage.co/query"
alpha_API_key = "xxxxxx"
alpha_params = {"function": "TIME_SERIES_INTRADAY",
        "symbol": defaultStock,
        "interval": "1min",
        "apikey": alpha_API_key
        }
response = requests.get(alpha_API_URL, params=alpha_params)
alpha_df = pd.DataFrame(response.json()['Time Series (1min)']).transpose()
#alpha_df.index = pd.to_datetime(alpha_df.index)


# create app
app = dash.Dash()
app.layout = html.Div( children=[
                html.H1(
                    children='Stocks',
                    style = {'textAlign': 'center' }
                ),
                html.Div(
                    children='stock ticker',
                    style = {'textAlign': 'center' }
                ),
                dcc.Input(
                    id = 'input', value = '', type = 'text'
                ),
                html.Div(
                    id = 'error-message', children =  ''
                ),
                html.Div( children=[
                    dcc.Graph(
                        id='example-graph'
                        ),
                    dcc.Graph(
                        id='daily-graph'
                        )
                ], style={'columnCount': 2}
                )
            ], style={'textAlign': 'center',
                     # 'backgroundColor': '#111111',
                      'color': '#69F7AB'})


## error stock ticker catch
@app.callback(
        Output(component_id = 'error-message', component_property = 'children'),
        [Input(component_id = 'input', component_property = 'value')]
        )
def error_raise(input_val):

    if len(input_val) == 0:
        return 'Please Enter Stock\'s name'

    stock = str(input_val)
    p = multiprocessing.Process(target=find_stock,  args=(stock,))
    p.start()
    p.join(1)  # wait the request for 1 second
    if p.is_alive():
        print "Request has been running for 1 seconds... let's kill it..."
        # Terminate
        p.terminate()
        p.join()
        return 'Ticker - {} - Request Failed: Please try other names'.format(stock)
    print "Ticker - {} -Request Success".format(stock)
    return ''


## plot static chart
@app.callback(
        Output(component_id = 'example-graph', component_property = 'figure'),
        [Input(component_id = 'input', component_property = 'value'),
         Input(component_id = 'error-message', component_property = 'children')]
        )
def update_graph(input_val,error_mes):
    global defaultdf
    global defaultStock

    error_mes = str(error_mes)
    if len(input_val) != 0 and len(error_mes) == 0 :

        stock = str(input_val)
        start = datetime.datetime(2016, 1, 1)
        end = datetime.datetime.now()
        df = web.DataReader(stock, 'morningstar' , start, end)
        defaultdf = df
        defaultStock = stock

        return {
                'data': [go.Scatter( x=df.index.get_level_values('Date') , y=df.Close )] ,
                'layout': { 'title': input_val + " from 2016",  }
                }
    return {
            'data': [go.Scatter( x=defaultdf.index.get_level_values('Date') , y=defaultdf.Close )] ,
            'layout': { 'title': defaultStock + " from 2016",  }
            }


## plot daily chart
@app.callback(
        Output(component_id = 'daily-graph', component_property = 'figure'),
        [Input(component_id = 'input', component_property = 'value'),
         Input(component_id = 'error-message', component_property = 'children')]
        )
def update_daily(input_val,error_mes):
    global alpha_df
    global defaultStock

    error_mes = str(error_mes)
    if len(input_val) != 0 and len(error_mes) == 0 :

        params = {"function": "TIME_SERIES_INTRADAY",
                  "symbol": str(input_val),
                  "interval": "1min",
                  "apikey": alpha_API_key
                 }
        response = requests.get(alpha_API_URL, params=params)
        response = response.json()

        # handel request error
        if 'Error Message' in response:
            pass
        else:
            alpha_df = pd.DataFrame(response['Time Series (1min)']).transpose()
            defaultStock = str(input_val)

    return {
            'data': [go.Scatter( x=alpha_df.index,
                                 y=alpha_df['4. close'],
                                 ) ],
            'layout': {
                'height': 430,
                'title': defaultStock + " Daily",
                'xaxis': {'showgrid': False}
                }
            }

if __name__ == '__main__':
    app.run_server(debug=True)


