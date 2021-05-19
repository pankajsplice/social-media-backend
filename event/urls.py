from django.urls import path
from rest_framework import routers
from django.urls import path, include
from event.views import EventViewSet, CategoryViewSet, VenueViewSet, FetchEventTicketMasterApiView, CommentViewSet, \
    LikeViewSet, SubscriptionViewSet, FollowViewSet, MessageViewSet, MemberViewSet, \
    GroupViewSet, EventGroupViewSet, EventSettingViewSet, GroupMemberViewSet
router = routers.DefaultRouter()

router.register(r'events', EventViewSet)
router.register(r'events-category', CategoryViewSet)
router.register(r'events-venue', VenueViewSet)
router.register(r'events-comment', CommentViewSet)
router.register(r'events-like', LikeViewSet)
router.register(r'events-subscription', SubscriptionViewSet)
router.register(r'events-follow', FollowViewSet)
router.register(r'events-message', MessageViewSet)
router.register(r'member', MemberViewSet)
router.register(r'group', GroupViewSet)
router.register(r'group-member', GroupMemberViewSet)
router.register(r'events-group', EventGroupViewSet)
router.register(r'events-setting', EventSettingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('fetch-events/', FetchEventTicketMasterApiView.as_view(), name="fetch_events"),
]
