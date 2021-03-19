from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from utils.models import ModelMixin
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()
# Create your models here.


class Event(ModelMixin):
    name = models.CharField(max_length=100, help_text=_('Event Name'))
    global_id = models.CharField(max_length=50, help_text=_('Global Event Id'))
    url = models.URLField(help_text=_('Event Url'), null=True, blank=True)
    price_min = models.CharField(max_length=10, help_text=_('Price Range Min'), null=True, blank=True)
    price_max = models.CharField(max_length=10, help_text=_('Price Range Max'), null=True, blank=True)
    event_status = models.CharField(max_length=30, help_text=_('Event Status'))
    currency = models.CharField(max_length=10, help_text=_('Currency'))
    image_json = models.JSONField()
    category = models.ForeignKey('Category', help_text=_('Event Category'), blank=True, null=True, on_delete=models.CASCADE)
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True)
    seatmap_url = models.CharField(max_length=255, help_text=_('Seat Map Url'), null=True, blank=True)
    timezone = models.CharField(max_length=30, help_text=_('Timezone'))
    time = models.TimeField(help_text=_('Event Timing'), blank=True, null=True)
    date = models.DateField(help_text=_('Event Date'), blank=True, null=True)
    description = models.TextField(help_text=_('Event Description'), null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


class Venue(ModelMixin):
    name = models.CharField(max_length=100, help_text=_('Venue Name'))
    global_id = models.CharField(max_length=50, help_text=_('Global Venue Id'))
    city = models.CharField(max_length=50, help_text=_('Venue Name'))
    address = models.CharField(max_length=100, help_text=_('Venue Address'))
    state_code = models.CharField(max_length=20, help_text=_('State Code'))
    state_name = models.CharField(max_length=50, help_text=_('State Name'))
    postal_code = models.CharField(max_length=10, help_text=_('Postal Code'))
    country_code = models.CharField(max_length=20, help_text=_('Country Code'))
    country_name = models.CharField(max_length=50, help_text=_('Country Name'))
    latitude = models.CharField(max_length=20, help_text=_('Latitude'), null=True, blank=True)
    longitude = models.CharField(max_length=20, help_text=_('Longitude'), null=True, blank=True)
    url = models.URLField(help_text=_('Venue Url'), null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)
