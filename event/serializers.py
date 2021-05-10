from event.models import Event, Category, Venue, Comment, Subscription, UserSubscription, Like,\
    Follow, Message, Member, Group, EventGroup, EventSetting
from utils.custom_mixin import QuerySetFilterMixin, CustomBaseSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EventSerializer(CustomBaseSerializer):
    like = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'name', 'global_id', 'url', 'price_min', 'price_max', 'event_status', 'currency',
                  'image_json', 'event_image', 'category', 'venue', 'seatmap_url', 'timezone', 'time', 'date',
                  'user', 'description', 'like', 'comment', 'group', 'created_by', 'updated_by', 'status',
                  'date_created', 'date_updated')

    def get_like(self, obj):
        like = Like.objects.filter(event_id=obj.id).count()
        return like

    def get_comment(self, obj):
        comment = Comment.objects.filter(event_id=obj.id).count()
        return comment

    def get_group(self, obj):
        group = EventGroup.objects.filter(event_id=obj.id).count()
        return group


class CategorySerializer(CustomBaseSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VenueSerializer(CustomBaseSerializer):
    class Meta:
        model = Venue
        fields = '__all__'


class CommentSerializer(CustomBaseSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'event', 'msg', 'verified', 'created_by', 'updated_by', 'status', 'username',
                  'date_created', 'date_updated' )

    def get_username(self, obj):
        user = User.objects.filter(id=obj.created_by.pk).get()
        username = "{} {}".format(user.first_name, user.last_name)
        return username


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
