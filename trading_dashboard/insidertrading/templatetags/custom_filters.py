from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return Decimal(value) * Decimal(arg)
    except:
        return ''
    
@register.filter
def sum(value, arg):
    try:
        return Decimal(value) + Decimal(arg)
    except:
        return ''