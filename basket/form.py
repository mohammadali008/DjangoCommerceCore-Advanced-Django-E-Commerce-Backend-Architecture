from django import  forms

from catalogue.models import Product


# --- Define AddToBasketForm --- #
class AddToBasketForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.default_objects.all(),
        widget=forms.HiddenInput
    )
    quantity = forms.IntegerField()
    # --- Define save method ---#
    def save(self,basket):
        basket.add(
            self.cleaned_data.get('product'),
            self.cleaned_data.get('quantity')
        )
        return basket

