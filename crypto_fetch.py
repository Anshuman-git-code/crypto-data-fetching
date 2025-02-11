import requests
import pandas as pd
import time
import schedule

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 50,
    "page": 1,
    "sparkline": False
}

CSV_FILE = "crypto_data.csv" 

def fetch_crypto_data():
    response = requests.get(API_URL, params=PARAMS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data:", response.status_code)
        return None

def analyze_data(data):
    df = pd.DataFrame(data)[["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]]

    top_5 = df.nlargest(5, "market_cap")

    avg_price = df["current_price"].mean()

    highest_change = df.nlargest(1, "price_change_percentage_24h")
    lowest_change = df.nsmallest(1, "price_change_percentage_24h")

    print("\nTop 5 Cryptocurrencies by Market Cap:\n", top_5)
    print("\nAverage Price of Top 50 Cryptos: $", round(avg_price, 2))
    print("\nHighest 24h Change:\n", highest_change)
    print("\nLowest 24h Change:\n", lowest_change)

    return df

def update_csv(data):

    df = analyze_data(data)

    df.to_csv(CSV_FILE, index=False)

    print("\nCSV file updated!")

def run_task():
    data = fetch_crypto_data()
    if data:
        update_csv(data)

schedule.every(5).minutes.do(run_task)

while True:
    schedule.run_pending()
    time.sleep(1)