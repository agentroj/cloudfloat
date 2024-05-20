from rest_framework import serializers
from .models import Invoice
import logging


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'amount_in_cents', 'timestamp_utc', 'statement_reference']

    def validate(self, data):
        if Invoice.objects.filter(invoice_number=data).exists():
            raise serializers.ValidationError("Invoice with this number already exists.")
        logging.warning(data)
        return data
