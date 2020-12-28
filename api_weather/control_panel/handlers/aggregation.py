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