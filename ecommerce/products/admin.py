from django.contrib import admin  # noqa: F401
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'size')


admin.site.register(Product, ProductAdmin)
