from django.db import models
from django.utils import timezone
from .const import SIZE_CHOICES
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
