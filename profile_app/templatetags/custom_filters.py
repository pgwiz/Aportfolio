# profile_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def format_date(value, default="Present"):
    """
    Formats a date object using the provided format string.
    If the value is None, returns the default value.
    """
    if value:
        return value.strftime("%Y-%m-%d")
    return default