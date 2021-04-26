from event.models import Event, Category, Venue, Comment, Subscription, UserSubscription, Like,\
    Follow, Message, Member, Group, EventGroup, EventSetting
from utils.custom_mixin import QuerySetFilterMixin, CustomBaseSerializer


class EventSerializer(CustomBaseSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class CategorySerializer(CustomBaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VenueSerializer(CustomBaseSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class CommentSerializer(CustomBaseSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(CustomBaseSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class SubscriptionSerializer(CustomBaseSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class UserSubscriptionSerializer(CustomBaseSerializer):
    class Meta:
        model = UserSubscription
        fields = '__all__'


class FollowSerializer(CustomBaseSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class MessageSerializer(CustomBaseSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MemberSerializer(CustomBaseSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class GroupSerializer(CustomBaseSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class EventGroupSerializer(CustomBaseSerializer):
    class Meta:
        model = EventGroup
        fields = '__all__'


class EventSettingSerializer(CustomBaseSerializer):
    class Meta:
        model = EventSetting
        fields = '__all__'
