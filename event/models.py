from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from utils.models import ModelMixin
User = get_user_model()
# Create your models here.



GENDER_SELECTOR = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other'),
)

EVENT_STATUS = (
    ('active','Active'),
    ('closed','Closed'),
)
P_EVENT_STATUS = (
    ('active','Active'),
    ('inactive','Inactive'),
)

class EventType(models.Model):
    name = models.CharField(max_length=30,help_text=_('Event Type'))

    def __str__(self):
        return "{}".format(self.name)



class EventModel(models.Model):
    type = models.ForeignKey(EventType,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,help_text=_('Event Title'))
    time = models.TimeField(help_text=_('Event Timing'))
    date = models.DateField(help_text=_('Event Date'))
    location = models.CharField(max_length=150,help_text=_('Event Location'))
    description = models.TextField(help_text=_('Event Description'))
    status = models.CharField(max_length=20,choices=EVENT_STATUS)
    likes = models.ManyToManyField(User, null=True, blank=True,related_name="users_like")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="event_created",null=True,blank=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __sr__(self):
        return "{}".format(self.title)


class EventParticipant(models.Model):
    event = models.ForeignKey(EventModel,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.id)



