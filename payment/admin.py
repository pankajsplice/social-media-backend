from django.contrib import admin
from payment.models import StripeCustomer
from utils.download_csv import ExportCsvMixin


class StripeCustomerAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = StripeCustomer
    list_display = ['id', 'user', 'customer', 'email', 'subscription', 'strip_subscription', 'status', 'created_at']
    actions = ["download_csv"]


admin.site.register(StripeCustomer, StripeCustomerAdmin)

