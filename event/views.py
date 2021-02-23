from django.shortcuts import render,redirect
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import EventParticipantSerializer,EventModelSerializer,EventTypeSerializer
from .models import EventModel,EventParticipant,EventType
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model


User = get_user_model()

# to create event-participants
class EventParticipantViewSet(viewsets.ModelViewSet):
    serializer_class = EventParticipantSerializer
    queryset = EventParticipant.objects.all()


# to create event
class EventModelViewSet(viewsets.ModelViewSet):
    serializer_class = EventModelSerializer
    queryset = EventModel.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['type', 'title','location','status']


# to create event-type
class EventTypeViewSet(viewsets.ModelViewSet):
    serializer_class = EventTypeSerializer
    queryset = EventType.objects.all()



# to count all like for particular event
class EventLikeApiView(APIView):
    def get(self,*args,**kwargs):
        id = self.kwargs['id']
        obj = EventModel.objects.filter(id=id).first()
        if obj:
            likes = obj.likes.count()
            return Response({'status':'success','count':likes})
        return Response({'status':'failed','message':'No event exists'})


# to count all active event
class ActiveEventApiView(APIView):
    def get(self,*args,**kwargs):
        events = EventModel.objects.filter(status='active').count()
        return Response({'status':'success','active_events':events})


# to count all active participants
class ActiveParticipantApiView(APIView):
    def get(self,*args,**kwargs):
        p = EventParticipant.objects.filter(event__status='active').count()
        return Response({'status':'success','active_events':p})


# to count all registered user
class TotalRegisteredUserApiView(APIView):
    def get(self,*args,**kwargs):
        p = User.objects.all().count()
        return Response({'status':'success','registered_users':p})