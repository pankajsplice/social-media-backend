from django.contrib import admin
from .models import EventModel,EventType,EventParticipant

# Register your models here.

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

class EventModelAdmin(admin.ModelAdmin):
    list_display = ['type','title','time','date','location','description','created_on','updated_on','created_by','updated_by']

class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event','user','created_on','updated_on']



admin.site.register(EventType,EventTypeAdmin)
admin.site.register(EventModel,EventModelAdmin)
admin.site.register(EventParticipant,EventParticipantAdmin)
