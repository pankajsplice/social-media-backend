from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _
from utils.models import ModelMixin
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()
# Create your models here.

SUBSCRIPTION_CHOICES = (
    (1, 'Monthly'),
    (6, 'HalfYearly'),
    (12, 'Yearly'),
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
    source = models.CharField(max_length=100, blank=True, null=True)
    recurring = models.BooleanField(default=False)
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
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text=_('Subscription Price'))
    validity = models.IntegerField(choices=SUBSCRIPTION_CHOICES, help_text=_('Validity in months'))
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_product_id = models.CharField(max_length=100, blank=True, null=True)
    paypal_plan_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text=_('Description'))

    def __str__(self):
        return "{}".format(self.name)


class Follow(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('Follower'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text=_('Event'))

    def __str__(self):
        return "{}".format(self.event.name)


class Message(ModelMixin):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True, help_text=_('sender'))
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver', null=True,  help_text=_('receiver'))
    msg = models.TextField(help_text=_('message'))
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ('timestamp',)


class Group(ModelMixin):
    name = models.CharField(max_length=255, help_text=_('Group Name'), unique=True)
    icon = models.ImageField(blank=True, null=True, help_text=_('Group Image'))
    description = models.TextField(help_text=_('Group Description'))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text=_('Event'), blank=True, null=True)
    member = models.ManyToManyField(User, blank=True, related_name='members')
    limit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class EventSetting(ModelMixin):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, help_text=_('Event'), null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, help_text=_('User'), null=True)
    recurring_event = models.ForeignKey('RecurringEvent', on_delete=models.SET_NULL,
                                        help_text=_('Recurring Date and Time'), blank=True, null=True)
    going = models.BooleanField(default=False)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    notification_type = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    read_status = models.BooleanField(default=False)
    accepted = models.BooleanField(blank=True, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class GroupMessage(ModelMixin):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='msg_sender', null=True, help_text=_('sender'))
    receiver = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='msg_receiver', null=True,  help_text=_('receiver'))
    msg = models.TextField(help_text=_('message'))
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ('timestamp',)


class RecurringEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, )
    time = models.TimeField(help_text=_('Event Timing'), blank=True, null=True)
    date = models.DateField(help_text=_('Event Date'), blank=True, null=True)

    def __str__(self):
        return "{} for {}".format(str(self.date), self.event)


GROUP_INVITATION_STATUS = (
    ('invited', 'Invited'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)


class GroupInvitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_by')
    invited_to = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=GROUP_INVITATION_STATUS)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status


class MessageSetting(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender_setting', null=True, help_text=_('sender'))
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='receiver_setting', null=True,
                                 blank=True, help_text=_('receiver'))
    gp_receiver = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='gp_receiver_setting', null=True,
                                    blank=True, help_text=_('group_receiver'))
    block = models.BooleanField(default=False)
    report = models.TextField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.block)
