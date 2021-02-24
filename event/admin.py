from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from utils.admin import CustomModelAdminMixin
from .models import EventModel, EventType, EventParticipant
from .resources import EventModelResource, EventParticipantResource, EventTypeResource


# Register your models here.
class EventTypeAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    resource_class = EventTypeResource
    search_fields = ['name']
    list_filter = ('status',)


class EventModelAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    resource_class = EventModelResource
    search_fields = ['type', 'title', 'time', 'date', 'location', 'description']
    list_filter = ('status', 'title')


class EventParticipantAdmin(CustomModelAdminMixin, ImportExportModelAdmin):
    resource_class = EventParticipantResource
    search_fields = ['event', 'participant']
    list_filter = ('status',)


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventModel, EventModelAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
