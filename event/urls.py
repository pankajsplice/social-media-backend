from django.urls import path
from rest_framework import routers
from django.urls import path, include
router = routers.DefaultRouter()
from event.views import EventViewSet, CategoryViewSet, VenueViewSet, FetchEventTicketMasterApiView, CommentViewSet, \
    LikeViewSet, SubscriptionViewSet, UserSubscriptionViewSet, FollowViewSet, MessageViewSet


router.register(r'events', EventViewSet)
router.register(r'events-category', CategoryViewSet)
router.register(r'events-venue', VenueViewSet)
router.register(r'events-comment', CommentViewSet)
router.register(r'events-like', LikeViewSet)
router.register(r'events-subscription', SubscriptionViewSet)
router.register(r'events-user-subscription', UserSubscriptionViewSet)
router.register(r'events-follow', FollowViewSet)
router.register(r'events-message', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('fetch-events/', FetchEventTicketMasterApiView.as_view(), name="fetch_events"),
]
