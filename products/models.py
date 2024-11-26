from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Category Description")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name", db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    pv_points = models.PositiveIntegerField(verbose_name="PV Points")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']