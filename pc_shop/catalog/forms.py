# forms.py
from django import forms
from .models import Product, AttributeValue

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Добавляем поля для каждого атрибута
            for attr_value in self.instance.attributevalue_set.all():
                field_name = f'attr_{attr_value.attribute.id}'
                field_value = attr_value.get_value()
                field_type = attr_value.attribute.attribute_type

                if field_type == 'boolean':
                    self.fields[field_name] = forms.BooleanField(
                        required=attr_value.attribute.required,
                        initial=field_value,
                        widget=forms.CheckboxInput()
                    )
                elif field_type == 'number':
                    self.fields[field_name] = forms.DecimalField(
                        required=attr_value.attribute.required,
                        initial=field_value,
                        widget=forms.NumberInput(attrs={'step': 'any'})
                    )
                else:
                    self.fields[field_name] = forms.CharField(
                        required=attr_value.attribute.required,
                        initial=field_value,
                        widget=forms.TextInput()
                    )