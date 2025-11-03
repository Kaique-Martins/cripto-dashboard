import requests
import pandas as pd
import urllib3
urllib3.disable_warnings()

def fetch_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1, "sparkline": False}

    response = requests.get(url, params=params, verify=False)
    data = response.json()

    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "price_change_percentage_24h"]]
    df.to_csv("data/cryptos.csv", index=False)
    return df
