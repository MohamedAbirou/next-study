from django import template

register = template.Library()

@register.filter
def k_format(value):
    if value >= 1000:
        value /= 1000
        return f'{value:.1f}k'
    return value