from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .const import SIZE_CHOICES

# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    creation_date = models.DateTimeField(default=timezone.now)
    
class Inventory(models.Model):

    size = models.CharField(
       max_length=5,
       choices=SIZE_CHOICES,
   )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)