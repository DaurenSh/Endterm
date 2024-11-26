import logging

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Transaction
from .serializers import TransactionSerializer

logger = logging.getLogger(__name__)

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Transaction list accessed by {request.user}")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Transaction created by {request.user}")
        return super().create(request, *args, **kwargs)


def transactions_list(request):
    transactions = Transaction.objects.all()
    logger.info(f"Transactions list accessed by {request.user}")
    return render(request, 'transactions/transactions_list.html', {'transactions': transactions})
