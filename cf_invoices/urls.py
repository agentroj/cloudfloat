from django.urls import path
from .views import upload_invoice, monthly_report

urlpatterns = [
    path('upload_invoice', upload_invoice, name='upload_invoice'),
    path('monthly_report', monthly_report, name='monthly_report'),
]
