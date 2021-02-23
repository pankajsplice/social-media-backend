from django.urls import path
from rest_framework import routers
from django.urls import path, include
router = routers.DefaultRouter()
from .views import EventTypeViewSet,EventModelViewSet,EventParticipantViewSet,EventLikeApiView,ActiveEventApiView,TotalRegisteredUserApiView


router.register(r'event-type',EventTypeViewSet)
router.register(r'event-participant',EventParticipantViewSet)
router.register(r'event',EventModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('like-count/<int:id>/',EventLikeApiView.as_view(),name="likes"),
    path('active-events/',ActiveEventApiView.as_view(),name="active_events"),
    path('active-participants/',ActiveEventApiView.as_view(),name="active_participants"),
    path('all-registered-users/',TotalRegisteredUserApiView.as_view(),name="active_participants"),
]
