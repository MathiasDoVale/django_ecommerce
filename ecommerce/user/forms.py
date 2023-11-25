from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, ShippingAddress, BillingAddress


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "phone_number")

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['country', 'state_province', 'postal_zip_code', 'city', 'street_address', 'building_number', 'postal_zip_code', 'city']

class BillingAddressForm(ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['country', 'state_province', 'postal_zip_code', 'city', 'street_address', 'building_number', 'postal_zip_code', 'city']
