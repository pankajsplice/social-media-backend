from django.urls import path
from rest_framework import routers
from django.urls import path, include
from event.views import EventViewSet, CategoryViewSet, VenueViewSet, FetchEventTicketMasterApiView, CommentViewSet, \
    LikeViewSet, SubscriptionViewSet, FollowViewSet, MessageViewSet, \
    PostGroupViewSet, GetGroupList, EventSettingViewSet, NotificationViewSet, MessageView,\
    MessageUser, GroupInvitationApi, GroupMessageListCreateView, RecurringEventChangeApiView, RecurringEventViewSet,\
    GroupInvitationViewset
from fcm_django.api.rest_framework import FCMDeviceCreateOnlyViewSet

router = routers.DefaultRouter()

router.register(r'events', EventViewSet)
router.register(r'events-category', CategoryViewSet)
router.register(r'events-venue', VenueViewSet)
router.register(r'events-comment', CommentViewSet)
router.register(r'events-like', LikeViewSet)
router.register(r'events-subscription', SubscriptionViewSet)
router.register(r'events-follow', FollowViewSet)
router.register(r'events-message', MessageViewSet)
router.register(r'post-group', PostGroupViewSet)
router.register(r'events-setting', EventSettingViewSet)
router.register(r'notification', NotificationViewSet)
router.register(r'push-notifications', FCMDeviceCreateOnlyViewSet)
router.register(r'recurring-events', RecurringEventViewSet)
router.register(r'group-invitation-setting', GroupInvitationViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('fetch-events/', FetchEventTicketMasterApiView.as_view(), name="fetch_events"),
    path('messages/<int:user>/<int:friend>', MessageView.as_view(), name='message-detail'),
    path('messages/', MessageView.as_view(), name='message-save'),
    path('message/user/<int:id>', MessageUser.as_view()),
    path('group-messages/', GroupMessageListCreateView.as_view(), name='group-message-save'),
    path('get-group/', GetGroupList.as_view()),
    path('group-invitation/', GroupInvitationApi.as_view(), name='group-invitation'),
    path('recurring-event-change/', RecurringEventChangeApiView.as_view(), name='recurring-event-change'),

]
