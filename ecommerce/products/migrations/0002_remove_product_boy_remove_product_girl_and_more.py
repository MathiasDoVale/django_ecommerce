# Generated by Django 4.2.5 on 2023-11-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='boy',
        ),
        migrations.RemoveField(
            model_name='product',
            name='girl',
        ),
        migrations.RemoveField(
            model_name='product',
            name='man',
        ),
        migrations.RemoveField(
            model_name='product',
            name='woman',
        ),
        migrations.AddField(
            model_name='image',
            name='boy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='girl',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='man',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='image',
            name='woman',
            field=models.BooleanField(default=False),
        ),
    ]