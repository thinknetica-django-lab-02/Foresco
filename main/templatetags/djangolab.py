# Custom filters and templates for djangolab course
import datetime
from django import template

register = template.Library()


@register.simple_tag
def current_time(format_string):
    """Returns current server time formatted by format_string"""
    return datetime.datetime.now().strftime(format_string)


@register.filter
def inverse_str(str):
    """Reverse symbols in str"""
    return str[::-1]
