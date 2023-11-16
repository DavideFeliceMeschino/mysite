from django import forms 
from shop.models import Prodotti




PRODUCT_QUANTITY_CHOCICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    quantita = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOCICES, coerce=int)
    override = forms.BooleanField(required=False, widget=forms.HiddenInput)