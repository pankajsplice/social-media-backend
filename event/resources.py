from import_export import resources
from event.models import *
from utils.admin import EXCLUDE_FOR_API


class EventTypeResource(resources.ModelResource):
    class Meta:
        model = EventType
        import_id_fields =('id', )
        exclude = EXCLUDE_FOR_API


class EventModelResource(resources.ModelResource):
    class Meta:
        model = EventModel
        import_id_fields = ('id', )
        exclude = EXCLUDE_FOR_API


class EventParticipantResource(resources.ModelResource):
    class Meta:
        model = EventParticipant
        import_id_fields = ('id', )
        exclude = EXCLUDE_FOR_API

