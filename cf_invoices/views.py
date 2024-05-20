from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.utils.timezone import make_aware
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.dateparse import parse_datetime

from .models import Invoice
from .serializers import InvoiceSerializer

import csv
import json
import pytz
import logging
import re
from datetime import datetime


@api_view(['POST'])
def upload_invoice(request):
    try:
        data = json.loads(request.body)

        invoice_number = data.get('invoice_number')
        amount_in_cents = data.get('amount_in_cents')
        timestamp_utc = data.get('timestamp_utc')
        statement_reference = data.get('statement_reference')

        # Validate Invoice Number Format
        if not re.match(r'^INV-\d{4}$', invoice_number):
            return JsonResponse({
                'error': 'Invalid invoice number format. It should be in the format INV-XXXX where XXXX is a four-digit number.'
                }, status=400)

        # Validate amount_in_cents
        if not isinstance(amount_in_cents, int) or amount_in_cents < 0:
            return JsonResponse({
                'error': 'Invalid amount_in_cents. It should be a positive integer.'
                }, status=400)

        # Validate timestamp_utc
        parsed_timestamp = parse_datetime(timestamp_utc)
        if not parsed_timestamp:
            return JsonResponse({
                'error': 'Invalid timestamp_utc format. It should be in ISO 8601 format.'
                }, status=400)

        # Ensure Timestamp is Has Timezone Info)
        if parsed_timestamp.tzinfo is None:
            return JsonResponse({
                'error': 'timestamp_utc must include timezone information.'
                }, status=400)

        # Check for Duplicate Invoice Number
        if Invoice.objects.filter(invoice_number=invoice_number).exists():
            return JsonResponse({
                'error': 'Invoice number already exists'
                }, status=409)

        # Create Invoice
        Invoice.objects.create(
            invoice_number=invoice_number,
            amount_in_cents=amount_in_cents,
            timestamp_utc=parsed_timestamp,
            statement_reference=statement_reference
        )

        return JsonResponse({
            'message': 'Invoice created successfully'}, status=201)

    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@api_view(['POST'])
def monthly_report(request):
    month = request.GET.get('month')
    try:
        year = int(request.GET.get('year'))
    except TypeError:
        year = datetime.now().year
    except ValueError:
        return JsonResponse({
            'error': 'Invalid Year'}, status=400)

    if month is None:
        return JsonResponse({
            'error': 'Month parameter is required'}, status=400)

    # Ensure Month is a String
    month = str(month).lower()

    # Convert Month Name to Number
    months = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    if month not in months:
        return JsonResponse({
            'error': 'Month parameter is invalid'}, status=400)

    month_number = months[month]

    # Get First and Last Day of the Month
    try:
        start_date = make_aware(datetime(year, month_number, 1))
    except ValueError:
        return JsonResponse({
            'error': 'Year is required'}, status=400)

    if month_number == 12:
        end_date = make_aware(datetime(year + 1, 1, 1))
    else:
        end_date = make_aware(datetime(year, month_number + 1, 1))

    # Filter Invoices for the Specified Month
    invoices = Invoice.objects.filter(
        timestamp_utc__gte=start_date,
        timestamp_utc__lt=end_date
        )

    # Create CSV Response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="monthly_report_{month}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Invoice Number',
        'Amount in Cents',
        'Timestamp UTC',
        'Statement Reference'
        ])

    for invoice in invoices:
        writer.writerow([
            invoice.invoice_number,
            invoice.amount_in_cents,
            invoice.timestamp_utc,
            invoice.statement_reference
            ])

    return response
