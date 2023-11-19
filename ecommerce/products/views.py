from django.shortcuts import render, redirect
from django.urls import reverse  # noqa: F401
from .forms import AddProductForm, InventoryForm, AddImageForm, EditItemForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Inventory, Product, Image
from django.db.models import ProtectedError
from django.contrib import messages


def home_view(request, gender=None):
    products = Product.objects.all().order_by('creation_date')
    gender_filters = {'man': {'man': True}, 'woman': {'woman': True}, 'girl': {'girl': True}, 'boy': {'boy': True}}
    data = []
    for product in products:
        filter_args = gender_filters.get(gender, {})
        filter_args['product_id'] = product.id
        image = Image.objects.filter(**filter_args).first()
        if image:
            data.append({'product': product, 'image': image})
    return render(request, "home.html", {'data': data})


def delete_product_view(request, force_delete_flag=None, product_id=None):
    product = Product.objects.get(id=product_id)
    if force_delete_flag == 1:
        Inventory.objects.filter(product_id=product_id).delete()
        # Delete images associated with this product from fileSystem
        images_list = Image.objects.filter(product_id=product_id)
        for item in images_list:
            item.image.delete()
        product.delete()
        return redirect("edit_product")
    if request.method == "GET":
        try:
            product.delete()
            images_list = Image.objects.filter(product_id=product_id)
            for item in images_list:
                item.image.delete()
            product = None
        except ProtectedError:
            messages.error(request, "There are items in inventory for this product.")
        if product is None:
            return redirect("edit_product")
        else:
            return redirect("edit_product_force_delete", force_delete_flag=0, product_id=product_id)


@staff_member_required
def add_product_view(request):
    product = None
    if request.method == 'POST':
        form_add_product = AddProductForm(request.POST)
        form_inventory = InventoryForm(request.POST)
        if form_add_product.is_valid() and form_inventory.is_valid():
            product = form_add_product.save()
            quantity = form_inventory.cleaned_data.get("quantity")
            sizes = form_inventory.cleaned_data.get("sizes")
            if quantity is None or quantity >= 0:
                Inventory.add_units(sizes, quantity or 0, product.id)
    else:
        form_add_product = AddProductForm()
        form_inventory = InventoryForm()
    return render(request, "administration/products/form_add_product.html",
                  {"form_add_product": form_add_product,
                   "form_inventory": form_inventory,
                   'product': product})


@staff_member_required
def edit_product_view(request, force_delete_flag=None, product_id=None):
    products = Product.objects.all().order_by('creation_date')
    inventory_items = list(Inventory.objects.all())
    data = [{'product': product, 'quantity': sum(item.product.id == product.id for item in inventory_items)} for product in products]
    return render(request, "administration/products/edit.html",
                  {'data': data,
                   'force_delete_product_id': product_id})


@staff_member_required
def edit_product_detail_view(request, product_id):
    product = Product.objects.get(id=product_id)
    form_add_product = AddProductForm(request.POST or None, instance=product)
    form_image = AddImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form_add_product.is_valid():
            product = form_add_product.save()
        if form_image.is_valid() and request.FILES:
            image = form_image.save(commit=False)
            image.product = product
            image.save()
    images = Image.objects.filter(product_id=product_id).order_by('id')
    return render(request, "administration/products/edit_detail.html",
                  {"form_add_product": form_add_product,
                   "form_image": form_image,
                   "images": images,
                   "product_id": product_id})


@staff_member_required
def add_item_inventory_view(request, product_id):
    product = Product.objects.get(id=product_id)
    form_inventory = InventoryForm(request.POST or None)
    if request.method == 'POST' and form_inventory.is_valid():
        quantity = form_inventory.cleaned_data.get("quantity", 0)
        sizes = form_inventory.cleaned_data.get("sizes")
        if quantity > 0:
            Inventory.add_units(sizes, quantity, product_id)
    items = Inventory.objects.filter(product_id=product_id).order_by('id').iterator()
    return render(request, "administration/inventory/items.html",
                  {'form_inventory': form_inventory,
                   'product': product,
                   'items': items})


@staff_member_required
def edit_item_inventory_view(request, item_id):
    item = Inventory.objects.get(id=item_id)
    if request.method == 'POST':
        form_edit_item = EditItemForm(request.POST, instance=item)
        if form_edit_item.is_valid():
            form_edit_item.save()
            return redirect(reverse('add_item_inventory', kwargs={'product_id': item.product_id}))
    else:
        form_edit_item = EditItemForm(instance=item)
    return render(request, "administration/inventory/edit_item.html",
                  {'form_edit_item': form_edit_item, 'item_id': item_id})


@staff_member_required
def delete_item_inventory_view(request, product_id, item_id):
    product = Product.objects.get(id=product_id)
    Inventory.objects.get(id=item_id).delete()
    if not Inventory.objects.filter(product_id=product_id).exists():
        product.has_item = False
        product.save()
    return redirect(reverse('add_item_inventory', kwargs={'product_id': product_id}))


@staff_member_required
def delete_image_view(request, product_id, image_id, gender):
    image = Image.objects.get(id=image_id)
    gender_attributes = {'man': 'man', 'woman': 'woman', 'boy': 'boy', 'girl': 'girl'}

    if gender in gender_attributes:
        setattr(image, gender_attributes[gender], False)
        image.save()

    # Only deletes the image if doesn't have a gender=True
    if not any(getattr(image, attr) for attr in gender_attributes.values()):
        image.image.delete()
        image.delete()

    return redirect(reverse('edit_product_detail', kwargs={'product_id': product_id}))

def product_detail_view(request, product_id_model):
    selected_product = Product.objects.get(id=product_id_model)
    similar_products = Product.objects.filter(brand=selected_product.brand, model=selected_product.model)

    data = []
    for product in similar_products:
        images = Image.objects.filter(product_id=product.id)
        items_inventory = Inventory.objects.filter(product_id=product.id).distinct('size')
        if images and items_inventory:
            data.append({'product': product, 'images': images, 'items_inventory': items_inventory})
    return render(request, "products/product_detail.html", {'data': data})