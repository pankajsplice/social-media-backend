from rest_framework import serializers
from event.models import EventModel,EventParticipant,EventType

class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = '__all__'

class EventParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = '__all__'

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'