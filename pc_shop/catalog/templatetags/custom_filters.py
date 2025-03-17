# catalog/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_attribute_value(attribute_values, attribute_name):
    for av in attribute_values:
        if av.attribute.name == attribute_name:
            return av.get_value()
    return None

@register.filter
def get(dictionary, key):
    return dictionary.get(key)