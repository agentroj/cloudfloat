from django.contrib import admin
from .models import Invoice
# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'amount_in_cents', 'timestamp_utc', 'statement_reference')
    search_fields = ('invoice_number', 'statement_reference')
    list_filter = ('timestamp_utc',)
