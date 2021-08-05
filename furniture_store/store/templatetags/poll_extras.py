from django import template

register = template.Library()


@register.filter
def mul(value1, value2):
    return round(value1 * value2, 2)
