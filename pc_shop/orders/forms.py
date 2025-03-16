from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'contact_phone', 'comment']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
        }