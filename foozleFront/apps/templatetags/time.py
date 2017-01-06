from datetime import datetime
from django import template

register = template.Library()

def hour(timestamp):
	date = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
	return date.strftime("%H:%M")


def seconds(timestampFail, timestampStep):
	dateFailed = datetime.strptime(timestampFail, '%Y-%m-%dT%H:%M:%S.%fZ')
	dateStep = datetime.strptime(timestampStep, '%Y-%m-%dT%H:%M:%S.%fZ')

	return  (dateStep - dateFailed).total_seconds()


def date(timestamp):
	return timestamp.split("T")[0]


def timestamp_hour(timestamp):
	return timestamp.strftime("%H:%M")


register.filter('hour', hour)
register.filter('seconds', seconds)
register.filter('timestamp_hour', timestamp_hour)