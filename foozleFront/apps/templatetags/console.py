from django import template

register = template.Library()

COLORS = {
	'log': 'success',
	'warn': 'warning',
	'error': 'danger',
}

ICONS = {
	'log': 'ti-info',
	'warn': 'ti-eye',
	'error': 'ti-heart-broken',
}



def color(severity):
	return COLORS[severity]


def icon(severity):
	return ICONS[severity]


register.filter('color', color)
register.filter('icon', icon)