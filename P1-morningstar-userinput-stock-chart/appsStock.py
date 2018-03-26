# -*- coding: utf-8 -*-
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# time handel
import multiprocessing
def find_stock(name):
    web.DataReader(name, 'morningstar', datetime.datetime(2015,1,1), datetime.datetime(2015,1,3))
    return

# default stock
defaultStock = 'GOOGL'
start = datetime.datetime(2015,1,1)
end = datetime.datetime.now()
defaultdf = web.DataReader(defaultStock, 'morningstar', start, end)

app = dash.Dash()
app.layout = html.Div(children=[
        html.H1(children='Morningstar Stocks'),

            html.Div(children='''
                        Please Input Company's Name
                            '''),
            dcc.Input(id = 'input', value = 'a', type = 'text'),
            html.Div( id = 'error-message', children =  ''),
            dcc.Graph(
                            id='example-graph',
                            )
            ])


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
    # wait the request for 1 seconds
    p.join(1)
    if p.is_alive():
        print "request has been running for 1 seconds... let's kill it..."
        # Terminate
        p.terminate()
        p.join()
        return '{} Request Failed: Please try other names'.format(stock)
    print "Request Success"
    return ''


@app.callback(
        Output(component_id = 'example-graph', component_property = 'figure'),
        [Input(component_id = 'input', component_property = 'value'),
         Input(component_id = 'error-message', component_property = 'children')]
        )
def update_graph(input_val,error_mes):
    error_mes = str(error_mes)
    print "hihere", len(error_mes)
    if len(input_val) != 0 and len(error_mes) == 0 :
        print "call", input_val
        stock = str(input_val)
        start = datetime.datetime(2015, 1, 1)
        end = datetime.datetime.now()
        df = web.DataReader(stock, 'morningstar' , start, end)

        return {
                'data': [go.Scatter( x=df.index.get_level_values('Date') , y=df.Close )] ,
                'layout': {
                    'title': input_val
                    }
                }
    return {
            'data': [go.Scatter( x=defaultdf.index.get_level_values('Date') ,
                y=defaultdf.Close )] ,
            'layout': {
                'title': defaultStock
                }
            }



if __name__ == '__main__':
    app.run_server(debug=True)



















































