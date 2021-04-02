# Custom filters and templates for djangolab course
import datetime
from django import template

from main.models import Product

register = template.Library()


@register.simple_tag
def current_time(format_string):
    """Returns current server time formatted by format_string"""
    return datetime.datetime.now().strftime(format_string)


@register.filter
def inverse_str(str):
    """Reverse symbols in str"""
    return str[::-1]


@register.filter
def product_type(type):
    """Return readable product type"""
    dct = {choice[0]: choice[1] for choice in Product.TYPECHOICES}
    return dct[type]


@register.filter
def page_concat(value, page_num):
    """Correctly concat page_num"""
    if value.find("?"):
        return f'{value}&page={page_num}'
    return f'{value}?page={page_num}'
