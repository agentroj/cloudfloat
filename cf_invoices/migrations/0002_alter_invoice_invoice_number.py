# Generated by Django 4.0 on 2024-05-20 03:04

import cf_invoices.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cf_invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(max_length=255, unique=True, validators=[cf_invoices.models.validate_invoice_number]),
        ),
    ]
