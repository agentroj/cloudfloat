import re
from django.core.exceptions import ValidationError
from django.db import models


def validate_invoice_number(value):
    if not re.match(r'^INV-\d{4}$', value):
        raise ValidationError(
            f'{value} is not a valid invoice number. It should be in the format INV-XXXX where XXXX is a four-digit number.'
        )


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=255, unique=True, validators=[validate_invoice_number])
    amount_in_cents = models.IntegerField()
    timestamp_utc = models.DateTimeField()
    statement_reference = models.CharField(max_length=18)

    def __str__(self):
        return self.invoice_number
