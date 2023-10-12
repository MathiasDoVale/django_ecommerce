from django.db import models  # noqa: F401
from django.utils import timezone

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    creation_date = models.DateTimeField(default=timezone.now)
    