# Generated by Django 4.2.5 on 2023-10-11 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_stock_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('2C', '2C'), ('3C', '3C'), ('4C', '4C'), ('5C', '5C'), ('6C', '6C'), ('7C', '7C'), ('8C', '8C'), ('9C', '9C'), ('10C', '10C'), ('10.5C', '10.5C'), ('11C', '11C'), ('11.5C', '11.5C')], max_length=5),
        ),
    ]