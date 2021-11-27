import ccxt
import plotly.graph_objects as go
import pandas as pd
import csv
import io
from datetime import datetime

binance = ccxt.binance({
    'apiKey': 'L7Auu8g0NcIqzn8VLtzz5K91r87oLIuhGnAXQuuEV8otOirqNX2qlWGSU9J6qrN8',
    'secret': 'RroWbqf9xr4WinrJIUuc6RLjeZl9SXU2kem4UIBFXoDzOA7WEo0Sydu9lxRNAdJx',
})

binance_markets = binance.load_markets()

from_date = '2021-07-13 00:00:00'
c_size = '1h'
n_candles = 500
save_path = "data/binance/"
from_timestamp = binance.parse8601(from_date)


for symbol in binance_markets:
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

