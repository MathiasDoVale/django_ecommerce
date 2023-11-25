from django.shortcuts import redirect, render  # noqa: F401
from .forms import CustomUserChangeForm, ShippingAddressForm, BillingAddressForm

def account_view(request):
    user = request.user
    shipping_address = user.shipping_addresses.first()
    billing_address = user.billing_addresses.first()

    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        shipping_form = ShippingAddressForm(request.POST, prefix='shipping', instance=shipping_address if shipping_address else None)
        billing_form = BillingAddressForm(request.POST, prefix='billing', instance=billing_address if billing_address else None)
        if user_form.is_valid() and shipping_form.is_valid() and billing_form.is_valid():
            user_form.save()

            shipping = shipping_form.save(commit=False)
            shipping.user = user
            shipping.save()

            billing = billing_form.save(commit=False)
            billing.user = user
            billing.save()   
    else:
        user_form = CustomUserChangeForm(instance=user)
        shipping_form = ShippingAddressForm(instance=shipping_address if shipping_address else None)
        billing_form = BillingAddressForm(instance=billing_address if billing_address else None)

    return render(request, 'registration/account.html', {'user': user, 'user_form': user_form, 'shipping_form': shipping_form, 'billing_form': billing_form})