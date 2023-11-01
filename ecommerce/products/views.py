from django.shortcuts import render, redirect  # noqa: F401
from .forms import AddProductForm, InventoryForm, GenderForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Gender, Inventory, Product

@staff_member_required
def add_product_view(request):
    form_add_product = AddProductForm(request.POST or None)
    form_inventory = InventoryForm(request.POST or None)
    form_gender = GenderForm(request.POST or None)
    if form_add_product.is_valid() and form_inventory.is_valid() and form_gender.is_valid():
        quantity = form_inventory.cleaned_data.get("quantity")
        sizes = form_inventory.cleaned_data.get("sizes")
        genders = form_gender.cleaned_data.get('genders')
        if quantity == None:
            quantity = 0
        if quantity != 0:
            product = form_add_product.save()
            for gender in genders:
                obj = Gender(gender=gender, product_id=product.id)
                obj.save()
            for size in sizes:
                i = 0
                while i < quantity:
                    obj = Inventory(size=size, product_id=product.id)
                    obj.save()

                    form_add_product = AddProductForm(request.POST or None)
                    form_inventory = InventoryForm(request.POST or None)
                    form_gender = GenderForm(request.POST or None)

                    i += 1
        form_add_product = AddProductForm()
        form_inventory = InventoryForm()
        form_gender = GenderForm()
    return render(request, "administration/products/form_add_product.html", {"form_add_product": form_add_product, "form_inventory": form_inventory, "form_gender": form_gender})

@staff_member_required
def images_adm_view(request):
    products = Product.objects.all()
    return render(request, "administration/products/images.html", {'products': products})
