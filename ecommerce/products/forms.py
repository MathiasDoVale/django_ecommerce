from django.forms import ModelForm, Textarea, IntegerField, MultipleChoiceField, CheckboxSelectMultiple, Form
from .models import Product, Inventory
from . const import GENDERS_CHOICES, SIZE_CHOICES

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]
        widgets = {
            "description": Textarea(attrs={"cols": 50, 
                                    "rows": 1}),
        }
        
class InventoryForm(Form):
    sizes = MultipleChoiceField(widget=CheckboxSelectMultiple(),
                                choices=SIZE_CHOICES)
    quantity = IntegerField()

class GenderForm(Form):
    genders = MultipleChoiceField(widget=CheckboxSelectMultiple,
                                          choices=GENDERS_CHOICES)
    