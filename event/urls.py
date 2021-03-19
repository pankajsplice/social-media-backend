from django.urls import path
from rest_framework import routers
from django.urls import path, include
router = routers.DefaultRouter()
from event.views import EventViewSet, CategoryViewSet, VenueViewSet, FetchEventTicketMasterApiView


router.register(r'events', EventViewSet)
router.register(r'events-category', CategoryViewSet)
router.register(r'events-venue', VenueViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('fetch-events/', FetchEventTicketMasterApiView.as_view(), name="fetch_events"),
]
