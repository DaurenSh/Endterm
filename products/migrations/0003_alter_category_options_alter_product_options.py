# Generated by Django 5.1.3 on 2024-11-22 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name']},
        ),
    ]