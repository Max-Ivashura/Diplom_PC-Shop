from django import template

register = template.Library()

@register.filter
def get_category_component(components, category):
    return components.filter(category=category).first()

@register.filter
def get_category_preview(category):
    return f"configurator/images/categories/{category.slug}.png"