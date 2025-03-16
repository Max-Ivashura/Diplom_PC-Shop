import django_filters
from .models import Product, AttributeValue


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'in_stock', 'min_price', 'max_price']

    @property
    def qs(self):
        parent_qs = super().qs
        # Пример добавления фильтрации по характеристикам
        attribute_filters = self.data.getlist('attribute')
        for attr_filter in attribute_filters:
            attr_id, value = attr_filter.split(':')
            parent_qs = parent_qs.filter(attributevalue__attribute_id=attr_id, attributevalue__value_string=value)
        return parent_qs