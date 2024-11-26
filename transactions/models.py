from django.db import models
from django.conf import settings
from products.models import Product


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('acceptance', 'Acceptance'),
        ('issuance', 'Issuance'),
    ]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name="Transaction Type")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions", db_index=True)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp", db_index=True)
    responsible_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} ({self.quantity})"
