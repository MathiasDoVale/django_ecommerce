from django.shortcuts import render, redirect  # noqa: F401
from .forms import AddProductForm, InventoryForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def add_product_view(request):
    form_add_product = AddProductForm(request.POST or None)
    form_inventory = InventoryForm(request.POST or None)
    if form_add_product.is_valid() and form_inventory.is_valid():
        quantity = form_inventory.cleaned_data.get("quantity")
        if quantity == None:
            quantity = 0
        if quantity is not 0:
            product = form_add_product.save()
            i = 0
            while i < quantity:
                product
                size = form_inventory.save(commit=False)
                size.product_id = product.id
                size.save()

                form_add_product = AddProductForm(request.POST or None)
                form_inventory = InventoryForm(request.POST or None)

                i += 1
        form_add_product = AddProductForm()
        form_inventory = InventoryForm()
    return render(request, "products/form_add_product.html", {"form_add_product": form_add_product, "form_inventory": form_inventory})
