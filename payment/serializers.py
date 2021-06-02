from payment.models import StripeCustomer
from rest_framework import serializers


class StripeCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripeCustomer
        fields = ('user', 'email', 'subscription', 'status')
