from catalog.models import AttributeValue
from django import template

register = template.Library()

@register.filter
def get_attribute_value(product, attribute):
    try:
        return AttributeValue.objects.get(product=product, attribute=attribute)
    except AttributeValue.DoesNotExist:
        return None

@register.filter
def get(dictionary, key):
    return dictionary.get(key)