from payment.models import StripeCustomer, PaypalCustomer
from rest_framework import serializers


class StripeCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeCustomer
        fields = ('user', 'email', 'subscription', 'status')


class PaypalCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaypalCustomer
        fields = ('user', 'subscription', 'status')