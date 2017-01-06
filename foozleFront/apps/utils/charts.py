import httpagentparser


def chart_by_top_browser(errors):
	data = {}

	for error in errors:
		browser = httpagentparser.simple_detect(error.data['environment']['userAgent'])[1]

		if browser not in data:
			 data[browser] = 0

		data[browser] += 1

	return data

