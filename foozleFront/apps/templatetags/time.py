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



register.filter('hour', hour)
register.filter('seconds', seconds)