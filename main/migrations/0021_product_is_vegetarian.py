# Generated by Django 4.2.5 on 2023-09-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_remove_product_is_vegetarian'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_vegetarian',
            field=models.BooleanField(default=True),
        ),
    ]
