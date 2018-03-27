import requests
import pandas as pd
API_URL = "https://www.alphavantage.co/query"
API_key = "JXXHFGAR98XVAEX0"
data = {   "function": "TIME_SERIES_INTRADAY",
            "symbol": "GOOGL",
            "interval": "1min",
<<<<<<< HEAD
            "apikey": API_key
=======
            "apikey": "XXX"
>>>>>>> 86b339698e607b8e84e4a4e63d596e60414083dd
         }
response = requests.get(API_URL, params=data)


try:
    print response.status_code
    print response.json()['Error Message']
except:
    print response.status_code
    f = pd.DataFrame(response.json()['Time Series (1min)']).transpose()
    f.index = pd.to_datetime(f.index)
    print f.head(1)




