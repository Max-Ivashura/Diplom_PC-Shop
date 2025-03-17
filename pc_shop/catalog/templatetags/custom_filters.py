from django import template

register = template.Library()

@register.filter
def get_attribute_value(attribute_values, attribute):
    try:
        return attribute_values.get(attribute=attribute)
    except:
        return None