from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from utils.models import ModelMixin
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()
# Create your models here.

SUBSCRIPTION_CHOICES = (
    ('1', 'Monthly'),
    ('3', 'Quarterly'),
    ('6', 'HalfYearly'),
    ('12', 'Yearly'),
)


class Event(ModelMixin):
    name = models.CharField(max_length=255, help_text=_('Event Name'))
    global_id = models.CharField(max_length=50, help_text=_('Global Event Id'))
    url = models.URLField(help_text=_('Event Url'), null=True, blank=True)
    price_min = models.CharField(max_length=10, help_text=_('Price Range Min'), null=True, blank=True)
    price_max = models.CharField(max_length=10, help_text=_('Price Range Max'), null=True, blank=True)
    event_status = models.CharField(max_length=30, help_text=_('Event Status'))
    currency = models.CharField(max_length=10, help_text=_('Currency'))
    image_json = models.JSONField(blank=True, null=True)
    event_image = models.ImageField(blank=True, null=True, help_text=_('Custom Event Image'))
    category = models.ForeignKey('Category', help_text=_('Event Category'), blank=True, null=True, on_delete=models.CASCADE)
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True)
    seatmap_url = models.CharField(max_length=255, help_text=_('Seat Map Url'), null=True, blank=True)
    timezone = models.CharField(max_length=30, help_text=_('Timezone'))
    time = models.TimeField(help_text=_('Event Timing'), blank=True, null=True)
    date = models.DateField(help_text=_('Event Date'), blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(help_text=_('Event Description'), null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return "{}".format(self.name)


class Venue(ModelMixin):
    name = models.CharField(max_length=255, help_text=_('Venue Name'))
    global_id = models.CharField(max_length=50, help_text=_('Global Venue Id'))
    city = models.CharField(max_length=100, help_text=_('Venue Name'))
    address = models.CharField(max_length=255, help_text=_('Venue Address'))
    state_code = models.CharField(max_length=20, help_text=_('State Code'))
    state_name = models.CharField(max_length=100, help_text=_('State Name'))
    postal_code = models.CharField(max_length=10, help_text=_('Postal Code'))
    country_code = models.CharField(max_length=20, help_text=_('Country Code'))
    country_name = models.CharField(max_length=100, help_text=_('Country Name'))
    latitude = models.CharField(max_length=20, help_text=_('Latitude'), null=True, blank=True)
    longitude = models.CharField(max_length=20, help_text=_('Longitude'), null=True, blank=True)
    url = models.URLField(help_text=_('Venue Url'), null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Comment(ModelMixin):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, )
    msg = models.TextField(help_text=_('message'))
    verified = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.event.name)


class Like(ModelMixin):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, )
    count = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.event.name)


class Subscription(ModelMixin):
    name = models.CharField(max_length=255, unique=True, help_text=_('Subscription Name'))
    price = models.DecimalField(max_digits=8, decimal_places=3, help_text=_('Subscription Price'))
    validity = models.IntegerField(choices=SUBSCRIPTION_CHOICES, help_text=_('Validity in months'))
    description = models.TextField(blank=True, null=True, help_text=_('Description'))

    def __str__(self):
        return "{}".format(self.name)


class UserSubscription(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    payment_amount = models.DecimalField(max_digits=8, decimal_places=3, help_text=_('Payment Amount'))
    payment_mode = models.CharField(max_length=100, blank=True, null=True, help_text=_('Mode of payment'))
    transaction_no = models.CharField(max_length=50, blank=True, null=True, unique=True, help_text=_('Transaction No.'))


class Follow(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('Follower'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text=_('Event'))


class Message(ModelMixin):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True, help_text=_('sender'))
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver', null=True,  help_text=_('receiver'))
    msg = models.TextField(help_text=_('message'))


class Member(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
    invited = models.BooleanField(default=False)

    def __del__(self):
        return "{}".format(self.user)


class Group(ModelMixin):
    name = models.CharField(max_length=255, help_text=_('Group Name'), unique=True)
    description = models.TextField(help_text=_('Group Description'))
    member = models.ManyToManyField(Member, blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class EventGroup(ModelMixin):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text=_('Event'))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, help_text=_('Select Group'))


class EventSetting(ModelMixin):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, help_text=_('Event'), null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, help_text=_('User'), null=True)
    going = models.BooleanField(default=False)