from payment.models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('user', 'email', 'subscription', 'status', 'source', 'transaction_id')

