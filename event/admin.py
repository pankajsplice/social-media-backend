from django.contrib import admin
from event.models import Event, Venue, Category, Comment, Like, Subscription, Message, Follow, \
    Member, Group, EventGroup, EventSetting, Notification
from utils.download_csv import ExportCsvMixin
from django_mptt_admin.admin import DjangoMpttAdmin


class EventAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Event
    list_display = ['id', 'name', 'global_id', 'url', 'price_min', 'price_max', 'event_status', 'currency', 'category',
                    'venue', 'timezone', 'time', 'date', 'user', 'source', 'description']
    actions = ["download_csv"]


class VenueAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Venue
    list_display = ['id', 'name', 'global_id', 'city', 'address', 'state_code', 'state_name', 'postal_code',
                    'country_code', 'country_name', 'latitude', 'longitude', 'url']
    actions = ["download_csv"]


class CategoryAdmin(DjangoMpttAdmin, ExportCsvMixin):
    model = Category
    list_display = ['id', 'name', 'parent']
    actions = ["download_csv"]


class CommentAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Comment
    list_display = ['id', 'event', 'msg', 'verified']
    actions = ["download_csv"]


class LikeAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Like
    list_display = ['id', 'event', 'count']
    actions = ["download_csv"]


class SubscriptionAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Subscription
    list_display = ['id', 'name', 'price', 'validity', 'description', 'stripe_product_id', 'stripe_price_id']
    actions = ["download_csv"]


class MessageAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Message
    list_display = ['id', 'sender', 'receiver', 'msg']
    actions = ["download_csv"]


class FollowAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Follow
    list_display = ['id', 'event', 'user']


class MemberAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Member
    list_display = ['id', 'user', 'invited']


class GroupAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Group
    list_display = ['id', 'name', 'description']


class EventGroupAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = EventGroup
    list_display = ['id', 'event', 'group']


class EventSettingAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = EventSetting
    list_display = ['id', 'event', 'user', 'going']


class EventNotification(admin.ModelAdmin, ExportCsvMixin):
    model = Notification
    list_display = ['id', 'event', 'user', 'notification_type', 'message', 'read_status', 'date_created']


admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(EventGroup, EventGroupAdmin)
admin.site.register(EventSetting, EventSettingAdmin)
admin.site.register(Notification, EventNotification)
