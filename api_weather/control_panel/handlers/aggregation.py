def temperature_aggregation(json_data):
	temp_list = []
	for datapoint in json_data:
	    temp_list.append(datapoint["temp"]['value'])
	    temperature_unit = datapoint["temp"]['units']

	average_temperature = round( (sum(temp_list) / len(temp_list) ) ,2 )

	temperature_aggregation_json = {
		"name": "Temperature",
		"avg" : average_temperature,
		"min" : min(temp_list),
		"max" : max(temp_list),
		"units": temperature_unit,
	}

	return temperature_aggregation_json


def windspeed_aggregation(json_data):
	wind_list = []
	for datapoint in json_data:
		wind_list.append( datapoint['wind_speed']['value'] )
		windspeed_unit = datapoint["wind_speed"]['units']

	average_wind = round( (sum(wind_list) / len(wind_list) ) ,2 )

	windspeed_aggregation_json = {
		"name": "Wind Speed",
		"avg" : average_wind,
		"min" : min(wind_list),
		"max" : max(wind_list),
		"units": windspeed_unit,
	}
	
	return windspeed_aggregation_json

def metric_aggregation(metric_name, metric_type, json_data):
	metric_list = []
	
	print("agg name:" + metric_name)
	print("agg type:"+metric_type)
	print(json_data)

	for datapoint in json_data:
		metric_list.append( datapoint[metric_type]['value'] )
		metric_unit = datapoint[metric_type]['units']
	
	metric_average = round( (sum(metric_list) / len(metric_list) ) ,2 )

	windspeed_aggregation_json = {
		"name": metric_name,
		"avg" : metric_average,
		"min" : min(metric_list),
		"max" : max(metric_list),
		"units": metric_unit,
	}
	

	return windspeed_aggregation_json