from django.shortcuts import render, redirect
from django.urls import reverse  # noqa: F401
from .forms import AddProductForm, InventoryForm, AddImageForm, EditItemForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Inventory, Product, Image
from django.db.models import ProtectedError
from django.contrib import messages


def home_view(request):
    # TODO
    return render(request, "home.html", {})


@staff_member_required
def delete_product_view(request, force_delete, product_id):
    if force_delete == 1:
        Inventory.objects.filter(product_id=product_id).delete()

        # Delete images associated with this product from fileSystem
        images_list = Image.objects.filter(product_id=product_id)
        for item in images_list:
            item.image.delete()

        Product.objects.filter(id=product_id).delete()
        return redirect("edit_product")
    if request.method == "GET":
        try:
            images_list = Image.objects.filter(product_id=product_id)
            for item in images_list:
                item.image.delete()

            Product.objects.filter(id=product_id).delete()
            product_id = None
        except ProtectedError:
            messages.error(request, "There are items in inventory for this product.")  # noqa: E501
        finally:
            if product_id is None:
                return redirect("edit_product")
            else:
                return redirect("edit_product_force_delete",
                                force_delete=0,
                                product_id=product_id)


@staff_member_required
def add_product_view(request):
    # product_id is used to know if a product was created.
    # In that case, it will show a comment to edit the new product.
    product_id = False
    if request.method == 'POST':
        form_add_product = AddProductForm(request.POST)
        form_inventory = InventoryForm(request.POST)
        if form_add_product.is_valid():
            form_add_product.save()
            if form_inventory.is_valid():
                quantity = form_inventory.cleaned_data.get("quantity")
                sizes = form_inventory.cleaned_data.get("sizes")
                if quantity is None:
                    quantity = 0
                if quantity != 0:
                    product = form_add_product.save()
                    Inventory.add_units(sizes, quantity, product.id)
                product_id = product.id

    form_add_product = AddProductForm()
    form_inventory = InventoryForm()
    return render(request, "administration/products/form_add_product.html",
                  {"form_add_product": form_add_product,
                   "form_inventory": form_inventory,
                   'product_id': product_id})


@staff_member_required
def edit_product_view(request, force_delete=None, product_id=None):
    # force_delete is not used here. But exists in html, so is a required.
    data = {}
    products = Product.objects.all().order_by('creation_date')
    inventory_items = list(Inventory.objects.all())
    i = 0
    for product in products:

        quantity = len(list(filter(lambda item: item.product.id == product.id, inventory_items)))  # noqa: E501
        data[i] = {'product': product, 'quantity': quantity}
        i += 1

    return render(request, "administration/products/edit.html",
                  {'data': data,
                   'force_delete_product_id': product_id})


@staff_member_required
def edit_product_detail_view(request, product_id):
    instance_product = Product.objects.get(id=product_id)
    images = Image.objects.filter(product=product_id)

    if request.method == 'POST':
        form_image = AddImageForm(request.POST, files=request.FILES)
        form_add_product = AddProductForm(request.POST, instance=instance_product)  # noqa: E501
        form_inventory = InventoryForm(request.POST)
        if form_add_product.is_valid():
            form_add_product.save()
            if form_inventory.is_valid():
                quantity = form_inventory.cleaned_data.get("quantity")
                sizes = form_inventory.cleaned_data.get("sizes")
                if quantity is None:
                    quantity = 0
                if quantity >= 0:
                    product = form_add_product.save()
                    Inventory.add_units(sizes, quantity, product.id)
        if form_image.is_valid():
            image = form_image.save(commit=False)
            image.product = instance_product
            image.save()

    form_add_product = AddProductForm(instance=instance_product)
    form_image = AddImageForm()
    return render(request, "administration/products/edit_detail.html",
                  {"form_add_product": form_add_product,
                   "form_image": form_image,
                   "images": images,
                   "product_id": product_id})


@staff_member_required
def add_item_inventory_view(request, product_id):
    product = Product.objects.get(id=product_id)
    items = Inventory.objects.filter(product_id=product_id).order_by('id').iterator()  # noqa: E501
    if request.method == 'POST':
        form_inventory = InventoryForm(request.POST)
        if form_inventory.is_valid():
            quantity = form_inventory.cleaned_data.get("quantity")
            sizes = form_inventory.cleaned_data.get("sizes")
            if quantity is None:
                quantity = 0
            if quantity > 0:
                Inventory.add_units(sizes, quantity, product_id)
    form_inventory = InventoryForm()
    return render(request, "administration/inventory/items.html",
                  {'form_inventory': form_inventory,
                   'product': product,
                   'items': items})


@staff_member_required
def edit_item_inventory_view(request, item_id):
    item = Inventory.objects.get(id=item_id)
    if request.method == 'POST':
        form_edit_item = EditItemForm(request.POST)
        if form_edit_item.is_valid():
            size = form_edit_item.cleaned_data.get("size")
            item.size = size
            item.save()
        return redirect(reverse('add_item_inventory', kwargs={'product_id': item.product_id}))  # noqa: E501
    form_edit_item = EditItemForm(initial={'size': item.size})
    return render(request, "administration/inventory/edit_item.html",
                  {'form_edit_item': form_edit_item,
                   'item_id': item_id})


@staff_member_required
def delete_item_inventory_view(request, product_id, item_id):
    Inventory.objects.get(id=item_id).delete()
    return redirect(reverse('add_item_inventory',
                            kwargs={'product_id': product_id}))


@staff_member_required
def delete_image_view(request, product_id, image_id, gender):
    image = Image.objects.get(id=image_id)
    if gender == 'man':
        image.man = False
    elif gender == 'woman':
        image.woman = False
    elif gender == 'boy':
        image.boy = False
    elif gender == 'girl':
        image.girl = False
    image.save()

    # Only deletes the image if doesn't have a gender associated
    if image.man is False and image.woman is False and image.girl is False and image.boy is False:  # noqa: E501
        image.image.delete()
        image.delete()
    return redirect(reverse('edit_product_detail',
                            kwargs={'product_id': product_id}))
