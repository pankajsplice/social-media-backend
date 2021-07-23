from django.db import models
from django.contrib.auth import get_user_model
from event.models import Subscription
User = get_user_model()


class Customer(models.Model):
    user = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    customer = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=150, default='')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
    third_party_subscription = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=100, default='')
    source = models.CharField(max_length=100, default='')
    transaction_id = models.CharField(max_length=255, default='')
    created_at = models.DateField(auto_now=True)

