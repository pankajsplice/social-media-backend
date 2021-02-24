from django.urls import path
from rest_framework import routers
from django.urls import path, include
router = routers.DefaultRouter()
from .views import EventTypeViewSet,EventModelViewSet,EventParticipantViewSet,ActiveEventApiView


router.register(r'event-type',EventTypeViewSet)
router.register(r'event-participant',EventParticipantViewSet)
router.register(r'event',EventModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('active-events/',ActiveEventApiView.as_view(),name="active_events"),
]
