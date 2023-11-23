from django.forms import (
    ModelForm,
    Textarea,
    IntegerField,
    MultipleChoiceField,
    CheckboxSelectMultiple,
    Form
)
from .models import Product, Image, Inventory
from . const import SIZE_CHOICES


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["brand", "model", "color", "description", "price"]
        widgets = {"description": Textarea(attrs={"cols": 50, "rows": 1})}


class InventoryForm(Form):
    sizes = MultipleChoiceField(widget=CheckboxSelectMultiple(),
                                choices=SIZE_CHOICES)
    quantity = IntegerField()


class EditItemForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["size"]


class AddImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('product', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
