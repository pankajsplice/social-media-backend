from django.contrib import admin
from payment.models import Customer
from utils.download_csv import ExportCsvMixin


class CustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Customer
    list_display = ['id', 'user', 'customer', 'email', 'subscription', 'third_party_subscription', 'status',
                    'source', 'transaction_id', 'created_at']
    actions = ["download_csv"]


admin.site.register(Customer, CustomerAdmin)

