from django import forms

from shipping.models import ShippingAddress


# --- Define Main Form ---#
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        # fields = ('user','city')
        exclude = ('user',)
        # fields = '__all__'
