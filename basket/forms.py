from django import forms

from .models import Product


class AddToBasketForm(forms.Form):
    product = forms.NodelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput)
    quantity = forms.IntegerField()

    def save(self, basket):
        basket.add(
            self.cleaned_data.get('product'),
            self.cleaned_data.get('quantity')
        )
        return basket

