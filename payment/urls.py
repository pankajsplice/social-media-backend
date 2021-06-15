from django.urls import path, include
from payment.views import CreateProductApi, GetStripePriceApi, StripeCustomerApiView, StripeCustomerViewSets,\
    GetPaymentDetails, ConfirmPaymentIntent
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'get-stripe-customer', StripeCustomerViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('create-product/', CreateProductApi.as_view(), name="create-product"),
    path('get-price/', GetStripePriceApi.as_view(), name="get-price"),
    path('stripe-customer-subscription/', StripeCustomerApiView.as_view(), name="stripe-customer"),
    path('get-payment-details/', GetPaymentDetails.as_view(), name="get-stripe-payment-details"),
    path('confirm-payment-intent/', ConfirmPaymentIntent.as_view(), name="confirm-payment-intent"),
]