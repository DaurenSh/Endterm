# Generated by Django 5.1.3 on 2024-11-22 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Timestamp'),
        ),
    ]