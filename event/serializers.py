from event.models import EventModel, EventParticipant, EventType
from utils.custom_mixin import QuerySetFilterMixin, CustomBaseSerializer


class EventModelSerializer(CustomBaseSerializer):
    class Meta:
        model = EventModel
        fields = '__all__'


class EventParticipantSerializer(CustomBaseSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'


class EventTypeSerializer(CustomBaseSerializer):
    class Meta:
        model = EventType
        fields = '__all__'
