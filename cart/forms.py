from django import forms 
from catalog.models import Product

product = Product()

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=product.stock, label='', widget = forms.NumberInput(attrs={'class': 'form-input mb-3 '}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)