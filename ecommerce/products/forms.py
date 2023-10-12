from django.forms import ModelForm, Textarea, IntegerField, BooleanField
from .models import Product, Inventory

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]
        widgets = {
            "description": Textarea(attrs={"cols": 50, 
                                    "rows": 1}),
        }
        
class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["size"]
    
    quantity = IntegerField()
        
    