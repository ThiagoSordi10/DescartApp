from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Order
from collect.models import Address, AddressDemand

class OrderForm(forms.ModelForm):

    quantity = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Quantity",
                "class": "form-control"
            }
        ))
    total_price = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Total price",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Order
        fields = ("total_price", "quantity", )

class OrderUpdateForm(OrderForm):

    status = forms.ChoiceField(
        choices = Order.STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                "placeholder": "Status",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Order
        fields = ("total_price", "quantity", )


class OrderAddressesForm(forms.ModelForm):

    addresses_choices= None
    addresses = forms.ModelMultipleChoiceField(label='Address', queryset=addresses_choices, required=True, widget=forms.CheckboxSelectMultiple(
            attrs={
                "placeholder": "Addresses",
                "style": "width:50%; height: 50%;"
            }
        ))
    order = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Order",
                "disabled": True,
                "class": "form-control"
            }
        ))  

    
    class Meta:
        model = AddressDemand
        fields = ("order", "addresses", )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        id = kwargs.pop('pk', None)
        super(OrderAddressesForm, self).__init__(*args, **kwargs)
        self.addresses_choices= Address.objects.filter(discarder = user.discarder)
        self.fields['addresses'].queryset = self.addresses_choices
        self.fields['addresses'].initial = [a.address.id for a in AddressDemand.objects.filter(demand_id=id)]
        self.fields['order'].initial = Order.objects.get(pk=id)
        self.fields['order'].required = False