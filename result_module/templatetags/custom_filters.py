import os
from django import template
from datetime import datetime
register = template.Library()

@register.filter(name='strftime')
def strftime(date, format_string):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')  # Convert the string to a datetime object
    return date.strftime(format_string)


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter
def filename(value):
    return os.path.basename(value.name)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")