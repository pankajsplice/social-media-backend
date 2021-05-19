from django.urls import path
from payment.views import CreateProductApi, GetStripePriceApi, StripeCustomerApiView

urlpatterns = [
    path('create-product/', CreateProductApi.as_view(), name="create-product"),
    path('get-price/', GetStripePriceApi.as_view(), name="get-price"),
    path('stripe-customer-subscription/', StripeCustomerApiView.as_view(), name="stripe-customer"),
]