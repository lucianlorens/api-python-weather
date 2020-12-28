import requests
import os
from dotenv import load_dotenv
from pathlib import Path 

import json

from datetime import datetime, timedelta


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

API_KEY = os.getenv("WEATHER_API_KEY")

url = "https://api.climacell.co/v3/weather/historical/station"

def get_climacell_data(latitude,longitude, fields_list ):
	
	fields_string = ','.join(fields_list)

	from datetime import datetime, timedelta

	now = datetime.now().replace(microsecond=0)

	yesterday = now - timedelta(days=1)

	querystring = {
		"lat": latitude,
		"lon": longitude,
		"unit_system": "si",
		"start_time": yesterday.isoformat(),
		"end_time": now.isoformat(),
		"fields": fields_string,
		"apikey": API_KEY
	}

	response = requests.request("GET", url, params=querystring)

	return json.loads(response.text)