import ccxt
import plotly.graph_objects as go
import pandas as pd
import csv
import io
from datetime import datetime

binance = ccxt.binance({
    'apiKey': 'wOc58t948tBbx8z6yeEL9CessrYnZa1LcbhNmncvuohEVDfSvMQKXsOyPXgmiDVJ',
    'secret': 'oypXsbwYMrZ7fNktAOHT6HGozW5eVzQrDVWbeubO4G0FyE4f4Zq9OXDUh2n492YU',
})

binance_markets = binance.load_markets()

from_date = '2021-11-30 15:00:00'
c_size = '15m'
n_candles = 1000
save_path = "data/binance/"
from_timestamp = binance.parse8601(from_date)

"""
for symbol in binance_markets:
	if "/BTC" in symbol:
		print("Fetching:", symbol)
		ohlcv_data = binance.fetch_ohlcv(symbol, c_size, from_timestamp, n_candles)
		with open(save_path+symbol.replace("/", "-")+".csv", "w", newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["", "Timestamp", "Open", "High", "Low", "Close", "Volume"])
			index = 0
			for epoch in ohlcv_data:
				epoch[0] = datetime.fromtimestamp(epoch[0] // 1000).strftime("%Y-%m-%d %H:%M:%S")
				writer.writerow([index] + epoch)
				index += 1



"""

for symbol in binance_markets:
	if "GRS/BTC" in symbol:
		print("Fetching:", symbol)
		ohlcv_data = binance.fetch_ohlcv(symbol, c_size, from_timestamp, n_candles)
		with open(save_path+"GRS-BTC7.csv", "w", newline='') as f:
			writer = csv.writer(f)
			writer.writerow(["", "Timestamp", "Open", "High", "Low", "Close", "Volume"])
			index = 0
			for epoch in ohlcv_data:
				epoch[0] = datetime.fromtimestamp(epoch[0] // 1000).strftime("%Y-%m-%d %H:%M:%S")
				if (True):
					writer.writerow([index] + epoch)
				index += 1
