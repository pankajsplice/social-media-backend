from django.urls import path, include
from payment.views import CreateProductApi, GetStripePriceApi, StripeCustomerApiView, StripeCustomerViewSets,\
    GetPaymentDetails, ConfirmPaymentIntent, GetLocalMinglePaymentDetails
from rest_framework import routers
from payment.paypal import PaypalProductListCreateApi, PaypalPlanListCreateApi, PaypalSubscriptionApi,\
    GetPaypalPaymentStatus, CancelPaypalSubscription

router = routers.DefaultRouter()

router.register(r'get-stripe-customer', StripeCustomerViewSets)

urlpatterns = [
    path('', include(router.urls)),
    path('create-product/', CreateProductApi.as_view(), name="create-product"),
    path('get-price/', GetStripePriceApi.as_view(), name="get-price"),
    path('stripe-customer-subscription/', StripeCustomerApiView.as_view(), name="stripe-customer"),
    path('get-payment-details/', GetPaymentDetails.as_view(), name="get-stripe-payment-details"),
    path('confirm-payment-intent/', ConfirmPaymentIntent.as_view(), name="confirm-payment-intent"),
    path('paypal-product/', PaypalProductListCreateApi.as_view(), name="paypal-product"),
    path('paypal-plan/', PaypalPlanListCreateApi.as_view(), name="paypal-plan"),
    path('paypal-subscription/', PaypalSubscriptionApi.as_view(), name="paypal-subscription"),
    path('get-paypal-subscription/', GetPaypalPaymentStatus.as_view(), name="get-paypal-subscription"),
    path('cancel-paypal-subscription/', CancelPaypalSubscription.as_view(), name="cancel-paypal-subscription"),
    path('local-mingle-payment-details/', GetLocalMinglePaymentDetails.as_view(), name="pay-detail"),
]