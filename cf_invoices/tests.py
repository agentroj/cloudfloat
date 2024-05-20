from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Invoice
import json


class InvoiceTests(TestCase):

    def test_valid_invoice_upload(self):
        data = {
            "invoice_number": "INV-1234",
            "amount_in_cents": 1000,
            "timestamp_utc": "2024-05-17T12:00:00Z",
            "statement_reference": "Reference1234"
        }
        response = self.client.post(reverse('upload_invoice'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Invoice.objects.filter(invoice_number="INV-1234").exists())

    def test_invalid_invoice_format(self):
        data = {
            "invoice_number": "INV-12A4",
            "amount_in_cents": 1000,
            "timestamp_utc": "2024-05-17T12:00:00Z",
            "statement_reference": "Reference1234"
        }
        response = self.client.post(reverse('upload_invoice'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid invoice number format', response.json()['error'])

    def test_duplicate_invoice_number(self):
        Invoice.objects.create(
            invoice_number="INV-1234",
            amount_in_cents=1000,
            timestamp_utc="2024-05-17T12:00:00Z",
            statement_reference="Reference1234"
        )
        data = {
            "invoice_number": "INV-1234",
            "amount_in_cents": 2000,
            "timestamp_utc": "2024-05-17T12:00:00Z",
            "statement_reference": "Reference5678"
        }
        response = self.client.post(reverse('upload_invoice'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertIn('Invoice number already exists', response.json()['error'])
