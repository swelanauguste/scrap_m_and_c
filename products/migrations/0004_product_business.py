# Generated by Django 5.1 on 2024-08-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='business',
            field=models.CharField(default='', max_length=255),
        ),
    ]
