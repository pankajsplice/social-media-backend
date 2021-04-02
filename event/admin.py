from django.contrib import admin
from event.models import Event, Venue, Category, Comment, Like, Subscription, UserSubscription
from utils.download_csv import ExportCsvMixin


class EventAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Event
    list_display = ['id', 'name', 'global_id', 'url', 'price_min', 'price_max', 'event_status', 'currency', 'category',
                    'venue', 'timezone', 'time', 'date', 'user', 'description']
    actions = ["download_csv"]


class VenueAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Venue
    list_display = ['id', 'name', 'global_id', 'city', 'address', 'state_code', 'state_name', 'postal_code',
                    'country_code', 'country_name', 'latitude', 'longitude', 'url']
    actions = ["download_csv"]


class CategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
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
    list_display = ['id', 'name', 'price', 'validity', 'description']
    actions = ["download_csv"]


class UserSubscriptionAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = UserSubscription
    list_display = ['id', 'user', 'subscription', 'payment_amount', 'payment_mode', 'transaction_no']
    actions = ["download_csv"]


admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
