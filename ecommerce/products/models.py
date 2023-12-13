from django.db import models
from django.utils import timezone
from .const import (
    SIZE_CHOICES,
    ORDERS_STATE_CHOICES
)
from django.conf import settings


# Create your models here.
class Product(models.Model):

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    creation_date = models.DateTimeField(default=timezone.now)
    has_item = models.BooleanField(default=False)


class Inventory(models.Model):

    size = models.CharField(max_length=5, choices=SIZE_CHOICES,)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    @classmethod
    def add_units(self, sizes, quantity, product_id):
        product = Product.objects.get(id=product_id)
        for size in sizes:
            i = 0
            while i < quantity:
                obj = Inventory(size=size, product_id=product_id)
                obj.save()
                product.has_item = True
                product.save()
                i += 1

    @classmethod
    def delete_item(self, product_id, item_id):
        product = Product.objects.get(id=product_id)
        Inventory.objects.get(id=item_id).delete()
        if not Inventory.objects.filter(product_id=product_id).exists():
            product.has_item = False
            product.save()    


class Image(models.Model):
    image = models.ImageField(upload_to="shoes", null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    man = models.BooleanField(default=False)
    woman = models.BooleanField(default=False)
    boy = models.BooleanField(default=False)
    girl = models.BooleanField(default=False)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES,)
    quantity = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=ORDERS_STATE_CHOICES, default='CREATED')
    date_ordered = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    item_inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.item_inventory.product.price * self.quantity