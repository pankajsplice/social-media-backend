from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

from utils.models import ModelMixin

User = get_user_model()
# Create your models here.


GENDER_SELECTOR = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

EVENT_STATUS = (
    ('active', 'Active'),
    ('closed', 'Closed'),
)
P_EVENT_STATUS = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)


class EventType(ModelMixin):
    name = models.CharField(max_length=30, help_text=_('Event Type'))

    def __str__(self):
        return "{}".format(self.name)


class EventModel(ModelMixin):
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, help_text=_('Event Title'))
    time = models.TimeField(help_text=_('Event Timing'))
    date = models.DateField(help_text=_('Event Date'))
    location = models.CharField(max_length=150, help_text=_('Event Location'))
    description = models.TextField(help_text=_('Event Description'))
    event_status = models.CharField(max_length=20, choices=EVENT_STATUS)
    likes = models.ManyToManyField(User, null=True, blank=True, related_name="users_like")

    def __sr__(self):
        return "{}".format(self.title)


class EventParticipant(ModelMixin):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)
