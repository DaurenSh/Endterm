from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    responsible_user_name = serializers.ReadOnlyField(source='responsible_user.username')

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'product', 'product_name', 'quantity', 'timestamp', 'responsible_user', 'responsible_user_name']