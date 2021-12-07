import requests
import json
import datetime

url = "https://pumpolymp.com:5001/api/allPumps"

payload = ""
headers = {
    'cookie': "_ga=GA1.2.57946753.1638255817; _gid=GA1.2.537223654.1638255817; uid=9d8df38b-e02d-4e6e-978b-69aedca112e0; utoken=TTOJeKwcMfcVQlmwisURxEjIeK/JsCUquwuW/FA7THs=",
    }

response = requests.request("GET", url, data=payload, headers=headers)

#cleaning data
data = response.text.encode("ascii", "ignore")
data = data.decode().replace("\\u", "")
json_data = json.loads(data)


count = 0
for obj in json_data:
	exchange = obj["exchange"]
	coin = obj["currency"]
	
	# convert time string to datetime obj
	try:
		pump_time = datetime.datetime.strptime(obj["signalTime"].replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
	except:
		pump_time = datetime.datetime.strptime(obj["signalTime"].replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S.%f')

	# filter for pumps that are only on the hour
	seconds = ["00", "01", "02", "03", "59", "58", "57"]
	if pump_time.strftime("%M") in seconds:
		if exchange == "Binance":
			print(exchange, coin, pump_time)
			count+=1
print(count)