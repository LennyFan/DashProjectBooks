import requests
#import alpha_vantage
import pandas as pd
API_URL = "https://www.alphavantage.co/query"

data = {   "function": "TIME_SERIES_INTRADAY",
            "symbol": "aaa",
            "interval": "1min",
            "apikey": "XXX"
         }
response = requests.get(API_URL, params=data)

print pd.DataFrame(response.json()['Time Series (1min)'])


#js = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=GOOGL&interval=1min&datatype%20=%20csv&apikey=JXXHFGAR98XVAEX0")
#print js.json()

