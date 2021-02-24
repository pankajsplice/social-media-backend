from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import authentication, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.custom_mixin import QuerySetFilterMixin

from .models import EventModel, EventParticipant, EventType
from .serializers import EventParticipantSerializer, EventModelSerializer, EventTypeSerializer

User = get_user_model()


# to create event-participants
class EventParticipantViewSet(QuerySetFilterMixin,viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventParticipantSerializer
    queryset = EventParticipant.objects.all()


# to create event
class EventModelViewSet(QuerySetFilterMixin,viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventModelSerializer
    queryset = EventModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['type', 'title', 'location', 'status']


# to create event-type
class EventTypeViewSet(QuerySetFilterMixin,viewsets.ModelViewSet):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()



# to count all active event
class ActiveEventApiView(APIView):
    def get(self, *args, **kwargs):
        events = EventModel.objects.filter(status='active').count()
        event_parts = EventParticipant.objects.filter(event__status='active').count()
        p = User.objects.all().count()
        return Response({'status': 'success', 'active_events': events,'active_participants':event_parts,'total_users':p})


